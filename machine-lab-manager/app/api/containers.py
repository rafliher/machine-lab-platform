# app/api/containers.py
import uuid
import base64
import datetime
from pydantic import BaseModel,IPvAnyAddress

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import httpx

from app.api.deps import get_db, get_current_admin
from app.models import (
    ContainerHost,
    HostStatus,
    Container,
    ContainerStatus,
    VPNProfile,
)

from app.api.hosts import Healthiness, compute_healthiness

from app.internal.vpn import (
    create_or_get_profile,
    apply_vpn_rule,
    remove_vpn_rule,
    remove_vpn_profile,
)

router = APIRouter(
    prefix="/containers",
    tags=["containers"],
    dependencies=[Depends(get_current_admin)],  # admin-only
)


class ContainerLaunchResponse(BaseModel):
    id: str
    host_id: uuid.UUID

class ContainerInfoResponse(BaseModel):
    id: str
    host_id: str
    user_id: str
    created_at: datetime.datetime
    name: str
    image: str
    status: str
    ip_address: IPvAnyAddress   # ← new field

@router.post(
    "/launch",
    response_model=ContainerLaunchResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Launch containerized environment",
    description="Upload and launch a Docker Compose environment for a user with automatic VPN integration."
)
async def launch_container(
    user_id: uuid.UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Launch a containerized environment for a user.
    
    This endpoint:
    1. Accepts a ZIP file containing Docker Compose configuration
    2. Selects an available container host with sufficient resources
    3. Creates or retrieves a VPN profile for the user
    4. Deploys the environment on the selected host
    5. Sets up VPN routing for secure access
    
    The ZIP file should contain:
    - docker-compose.yml or docker-compose.yaml
    - Any additional files referenced in the compose file
    - Optional Dockerfile(s) for custom images
    """
    # 1) Read & base64-encode the ZIP
    data = await file.read()
    encoded_zip = base64.b64encode(data).decode()

    # 2) Pick a healthy host with capacity
    stmt = select(ContainerHost).where(
        ContainerHost.status != HostStatus.offline,
        ContainerHost.cpu_percent < 90,
        ContainerHost.mem_percent < 90,
        ContainerHost.current_containers < ContainerHost.max_containers
    ).order_by(ContainerHost.current_containers)
    host = (await db.execute(stmt)).scalar_one_or_none()
    if not host:
        raise HTTPException(status_code=503, detail="No available host")

    # 3) Create or fetch the user's VPN profile, catching any errors
    try:
        user_ovpn_path = await create_or_get_profile(db, str(user_id))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create VPN profile for user {user_id}: {e}"
        )

    # 4) Load the VPNProfile record so we know the assigned IP
    stmt = select(VPNProfile).where(
        VPNProfile.client_name == str(user_id),
        VPNProfile.revoked == False
    )
    user_prof = (await db.execute(stmt)).scalar_one_or_none()
    if not user_prof:
        raise HTTPException(status_code=500, detail="User VPN profile missing")

    # 5) Pre-generate a container ID & create its VPN profile, again catching errors
    container_id = str(uuid.uuid4())
    try:
        cont_ovpn_path = await create_or_get_profile(db, container_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create VPN profile for container {container_id}: {e}"
        )

    stmt = select(VPNProfile).where(
        VPNProfile.client_name == container_id,
        VPNProfile.revoked == False
    )
    cont_prof = (await db.execute(stmt)).scalar_one_or_none()
    if not cont_prof:
        raise HTTPException(status_code=500, detail="Container VPN profile missing")

    with open(cont_ovpn_path, "rb") as f:
        encoded_vpn_container = base64.b64encode(f.read()).decode()

    # 6) Tell the host agent to start the container
    agent_url = f"http://{host.ip}:{host.api_port}/agent/containers"
    payload = {
        "name": container_id,
        "docker_zip_base64": encoded_zip,
        "vpn_conf_base64": encoded_vpn_container,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            agent_url,
            json=payload,
            headers={"X-Server-Key": host.cred_ref},
            timeout=30.0,
        )

    if resp.status_code != status.HTTP_201_CREATED:
        text = resp.text
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Agent failed to launch container: {text}"
        )

    # 7) Persist in our DB
    container = Container(
        id=container_id,
        user_id=user_id,
        host_id=host.id,
        name=container_id,
        status=ContainerStatus.running,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(container)
    host.current_containers += 1
    await db.commit()

    # 8) Allow only user↔container over tun0
    apply_vpn_rule(user_prof.ip_address, cont_prof.ip_address)

    return ContainerLaunchResponse(id=container_id, host_id=host.id)

@router.post(
    "/{container_id}/restart",
    status_code=status.HTTP_200_OK,
    summary="Restart container",
    description="Restart an existing container environment."
)
async def restart_container(
    container_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Restart a container environment.
    
    This sends a restart command to the container host where the
    container is running. The container will be stopped and started again.
    """
    # 1) Lookup the container record
    stmt = select(Container).where(Container.id == container_id)
    cont = (await db.execute(stmt)).scalar_one_or_none()
    if not cont:
        raise HTTPException(status_code=404, detail="Container not found")

    # 2) Find its host
    host = await db.get(ContainerHost, cont.host_id)
    if not host:
        raise HTTPException(status_code=500, detail="Host missing")

    # 3) Forward to the host agent
    agent_url = (f"http://{host.ip}:{host.api_port}"
                 f"/agent/containers/{cont.name}/restart")
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            agent_url,
            headers={"X-Server-Key": host.cred_ref},
            timeout=30.0,
        )
    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Agent restart failed: {resp.json()}"
        )

    # 4) Update status
    cont.status = ContainerStatus.running
    await db.commit()
    return {"detail": "Container restarted successfully"}


@router.delete(
    "/{container_id}",
    status_code=status.HTTP_200_OK,
    summary="Stop and remove container",
    description="Stop, remove, and clean up a container environment along with its VPN access."
)
async def stop_container(
    container_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Stop and completely remove a container environment.
    
    This operation:
    1. Stops and removes the container from the host
    2. Removes VPN routing rules
    3. Revokes the container's VPN profile
    4. Updates host capacity counters
    5. Removes the container record from the database
    """
    # 1) Lookup the container record
    stmt = select(Container).where(Container.id == container_id)
    cont = (await db.execute(stmt)).scalar_one_or_none()
    if not cont:
        raise HTTPException(status_code=404, detail="Container not found")

    # 2) Find its host
    host = await db.get(ContainerHost, cont.host_id)
    if not host:
        raise HTTPException(status_code=500, detail="Host missing")

    # 3) Tell the host agent to remove it
    agent_url = f"http://{host.ip}:{host.api_port}/agent/containers/{cont.name}"
    async with httpx.AsyncClient() as client:
        resp = await client.delete(
            agent_url,
            headers={"X-Server-Key": host.cred_ref},
            timeout=30.0,
        )
    if resp.status_code not in (200, 202, 204, 404):
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Agent delete failed: {resp.json()}"
        )

    # 4) Tear down VPN routing and profile
    await remove_vpn_profile(db, cont.id)

    # 5) Update DB
    await db.delete(cont)
    host.current_containers = max(0, host.current_containers - 1)
    await db.commit()
    return {"detail": "Container stopped and removed successfully"}


@router.get(
    "/{container_id}",
    response_model=ContainerInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Inspect a container’s status"
)
async def inspect_container(
    container_id: str,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Container).where(Container.id == container_id)
    cont = (await db.execute(stmt)).scalar_one_or_none()
    if not cont:
        raise HTTPException(status_code=404, detail="Container not found")

    host = await db.get(ContainerHost, cont.host_id)
    if not host:
        raise HTTPException(status_code=500, detail="Host missing")

    agent_url = f"http://{host.ip}:{host.api_port}/agent/containers"
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            agent_url,
            headers={"X-Server-Key": host.cred_ref},
            timeout=10.0,
        )
    live = resp.json()
    
    info = next((c for c in live if cont.name in c["name"] ), None)
    if not info:
        raise HTTPException(status_code=404, detail="Container not running")

    vpn_stmt = select(VPNProfile).where(
        VPNProfile.client_name == container_id,
        VPNProfile.revoked == False
    )
    vpn_prof = (await db.execute(vpn_stmt)).scalar_one_or_none()
    if not vpn_prof:
        raise HTTPException(status_code=500, detail="VPN profile missing")

    return ContainerInfoResponse(
        id=container_id,
        host_id=str(cont.host_id),
        user_id=str(cont.user_id),
        created_at=cont.created_at,
        name=info["name"],
        image=info.get("image", ""),
        status=info.get("status", ""),
        ip_address=vpn_prof.ip_address
    )


@router.get(
    "/",
    # response_model=list[ContainerInfoResponse],
    status_code=status.HTTP_200_OK,
    summary="List all containers",
    description="Retrieve a list of all containers managed by the platform."
)
async def list_all_containers(
    db: AsyncSession = Depends(get_db),
):
    """
    Get a list of all containers in the system.
    
    Returns basic information about each container including:
    - Container ID and name
    - Associated user ID
    - Host assignment
    - Creation timestamp
    - Current status
    """
    # 1) Fetch all Container records
    stmt = select(Container)
    result = await db.execute(stmt)
    containers = result.scalars().all()
    
    return containers
