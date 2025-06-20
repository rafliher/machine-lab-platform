import os
import tempfile
import zipfile
import base64
import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from docker import DockerClient
import psutil

from app.api.deps import get_server_key
from app.core.config import settings

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
    dependencies=[Depends(get_server_key)],  # protect all agent routes
)

# Initialize Docker client
client = DockerClient(base_url=settings.docker_socket)


class ContainerInfo(BaseModel):
    id: str
    name: str
    image: str
    status: str
    ports: dict[str, list[dict[str,int]]]


@router.get("/containers", response_model=list[ContainerInfo])
def list_containers():
    ctrs = client.containers.list(all=True)
    return [
        ContainerInfo(
            id=c.id,
            name=c.name,
            image=c.image.tags[0] if c.image.tags else "",
            status=c.status,
            ports=c.ports
        ) for c in ctrs
    ]


class StartContainerReq(BaseModel):
    name: str
    image: str | None = None
    port_map: dict[int,int] = Field(..., description="host_port:container_port")
    docker_zip_base64: str | None = Field(
        None,
        description="Optional base64-encoded zip of Docker context"
    )


@router.post("/containers", status_code=status.HTTP_202_ACCEPTED)
def start_container(req: StartContainerReq):
    # Build image from zip if provided
    image_ref = req.image
    if req.docker_zip_base64:
        data = base64.b64decode(req.docker_zip_base64)
        with tempfile.TemporaryDirectory() as tmp:
            zip_path = os.path.join(tmp, "ctx.zip")
            with open(zip_path, "wb") as f:
                f.write(data)
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(tmp)
            image, _ = client.images.build(path=tmp, rm=True)
            image_ref = image.tags[0] if image.tags else image.id

    # Map ports
    ports = {f"{ctr}/tcp": host for host, ctr in req.port_map.items()}
    container = client.containers.run(
        image_ref,
        name=req.name,
        detach=True,
        ports=ports
    )
    return JSONResponse({"id": container.id, "status": container.status})


@router.delete("/containers/{container_id}", status_code=status.HTTP_202_ACCEPTED)
def stop_remove_container(container_id: str):
    try:
        c = client.containers.get(container_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Container not found")
    c.stop()
    c.remove()
    return JSONResponse({"id": container_id, "status": "removed"})


@router.patch("/containers/{container_id}/restart", status_code=status.HTTP_200_OK)
def restart_container(container_id: str):
    try:
        c = client.containers.get(container_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Container not found")
    c.restart()
    return JSONResponse({"id": container_id, "status": c.status})


@router.get("/health", status_code=status.HTTP_200_OK)
def health():
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    running = len(client.containers.list())
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.5)
    return {
        "uptime_seconds": int(uptime.total_seconds()),
        "running_containers": running,
        "mem_percent": mem.percent,
        "cpu_percent": cpu
    }
