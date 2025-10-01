import os
import subprocess
import tempfile
import zipfile
import base64
import shutil
import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import docker
import psutil

from app.api.deps import get_server_key
from app.core.config import settings

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
    dependencies=[Depends(get_server_key)],  # protect all agent routes
)

# Initialize Docker client
client = docker.from_env()

# Base dir for all compose projects
WORK_DIR = "/opt/containers"
os.makedirs(WORK_DIR, exist_ok=True)


# ─── Schemas ────────────────────────────────────────────────────────────

class ContainerInfo(BaseModel):
    id: str
    name: str
    image: str
    status: str


class StartContainerReq(BaseModel):
    name: str
    docker_zip_base64: str
    vpn_conf_base64: str


class ActionResponse(BaseModel):
    name: str
    status: str


# ─── Existing: list containers ──────────────────────────────────────────

@router.get("/containers", response_model=list[ContainerInfo])
def list_containers():
    ctrs = client.containers.list()
    return [
        ContainerInfo(
            id=c.id,
            name=c.name,
            image=c.image.tags[0] if c.image.tags else "",
            status=c.status,
        ) for c in ctrs
    ]


# ─── New: start from Docker‐Compose + VPN conf ──────────────────────────

@router.post(
    "/containers",
    response_model=ActionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Unpack & docker compose up -d a new environment"
)
def start_container(req: StartContainerReq):
    work_dir = os.path.join(WORK_DIR, req.name)

    # 1) Remove old project folder if exists
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
    os.makedirs(work_dir)

    # 2) Extract the Docker Compose ZIP
    ctx_zip = os.path.join(work_dir, "context.zip")
    with open(ctx_zip, "wb") as f:
        f.write(base64.b64decode(req.docker_zip_base64))
    with zipfile.ZipFile(ctx_zip, "r") as z:
        z.extractall(work_dir)
    os.remove(ctx_zip)

    # 3) Write the VPN profile into the project
    vpn_path = os.path.join(work_dir, "vpn.ovpn")
    with open(vpn_path, "wb") as f:
        f.write(base64.b64decode(req.vpn_conf_base64))

    # 4) Launch with Docker Compose
    try:
        subprocess.run(
            ["docker", "compose", "up", "-d"],
            cwd=work_dir,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"'docker compose up' failed: {e}"
        )

    return ActionResponse(name=req.name, status="started")


# ─── New: rebuild & restart ────────────────────────────────────────────

@router.post(
    "/containers/{name}/restart",
    response_model=ActionResponse,
    summary="Rebuild & restart an existing environment"
)
def restart_container(name: str):
    work_dir = os.path.join(WORK_DIR, name)
    if not os.path.isdir(work_dir):
        raise HTTPException(status_code=404, detail="Environment not found")

    try:
        # Rebuild images
        subprocess.run(
            ["docker", "compose", "build"],
            cwd=work_dir,
            check=True
        )
        # Restart services
        subprocess.run(
            ["docker", "compose", "up", "-d"],
            cwd=work_dir,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Restart failed: {e}"
        )

    return ActionResponse(name=name, status="restarted")


# ─── New: down & remove ─────────────────────────────────────────────────

@router.delete(
    "/containers/{name}",
    response_model=ActionResponse,
    summary="Down & remove the environment"
)
def remove_container(name: str):
    work_dir = os.path.join(WORK_DIR, name)
    if not os.path.isdir(work_dir):
        raise HTTPException(status_code=404, detail="Environment not found")

    try:
        # Shut down and remove volumes but keep images for build cache
        subprocess.run(
            ["docker", "compose", "down", "--volumes"],
            cwd=work_dir,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"'docker compose down' failed: {e}"
        )

    # Finally, delete the directory
    shutil.rmtree(work_dir)

    return ActionResponse(name=name, status="removed")


# ─── Existing: health check ─────────────────────────────────────────────

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
