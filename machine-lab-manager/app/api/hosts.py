from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, conint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import datetime
import uuid

from app.models import ContainerHost, HostStatus, APIKey, APIKeyOwner
from app.api.deps import get_db, get_current_admin, get_server_key
from app.core.security import hash_token, create_admin_token
import enum

router = APIRouter(
    prefix="/hosts",
    tags=["hosts"],
)

# ─── Pydantic Schemas ────────────────────────────────────────────────────


class Healthiness(str, enum.Enum):
    offline = "offline"
    healthy = "healthy"
    warning = "warning"
    critical = "critical"


def compute_healthiness(status: HostStatus, cpu: int, mem: int) -> Healthiness:
    if status == HostStatus.offline:
        return Healthiness.offline
    if cpu >= 90 or mem >= 90:
        return Healthiness.critical
    if cpu >= 75 or mem >= 75:
        return Healthiness.warning
    return Healthiness.healthy


class HostBase(BaseModel):
    hostname: str
    ip: str
    ssh_port: conint(gt=0, lt=65536) = 22
    api_port: conint(gt=0, lt=65536) = 8000
    max_containers: conint(gt=0)


class HeartbeatRequest(BaseModel):
    cpu: int
    mem: int
    containers: int


class HostCreate(HostBase):
    pass


class HostUpdate(BaseModel):
    hostname: str | None = None
    ip: str | None = None
    ssh_port: conint(gt=0, lt=65536) | None = None
    api_port: conint(gt=0, lt=65536) | None = None
    max_containers: conint(gt=0) | None = None


class HostInfo(HostBase):
    id: uuid.UUID
    current_containers: int
    status: HostStatus
    last_seen: datetime.datetime | None
    cpu_percent: int
    mem_percent: int
    healthiness: Healthiness

    class Config:
        orm_mode = True


class HostRegisterResponse(BaseModel):
    host_id: uuid.UUID
    server_key: str


class HostStatusResponse(BaseModel):
    host_id: uuid.UUID
    status: HostStatus
    last_seen: datetime.datetime | None
    cpu_percent: int
    mem_percent: int
    healthiness: Healthiness
    current_containers: int


# ─── Endpoints ─────────────────────────────────────────────────────────


@router.get(
    "/", response_model=list[HostInfo], dependencies=[Depends(get_current_admin)]
)
async def list_hosts(db: AsyncSession = Depends(get_db)):
    stmt = select(ContainerHost)
    res = await db.execute(stmt)
    hosts = res.scalars().all()

    out: list[HostInfo] = []
    for h in hosts:
        health = compute_healthiness(h.status, h.cpu_percent, h.mem_percent)
        out.append(
            HostInfo(
                id=h.id,
                hostname=h.hostname,
                ip=h.ip,
                ssh_port=h.ssh_port,
                api_port=h.api_port,
                max_containers=h.max_containers,
                current_containers=h.current_containers,
                cpu_percent=h.cpu_percent,
                mem_percent=h.mem_percent,
                status=h.status,
                last_seen=h.last_seen,
                healthiness=health,
            )
        )
    return out


@router.get(
    "/{host_id}/status",
    response_model=HostStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Fetch status, last_seen & container count for a host",
    dependencies=[Depends(get_current_admin)],
)
async def get_host_status(
    host_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(ContainerHost).where(ContainerHost.id == host_id)
    res = await db.execute(stmt)
    h = res.scalar_one_or_none()
    if not h:
        raise HTTPException(status_code=404, detail="Host not found")

    health = compute_healthiness(h.status, h.cpu_percent, h.mem_percent)
    return HostStatusResponse(
        host_id=h.id,
        status=h.status,
        last_seen=h.last_seen,
        current_containers=h.current_containers,
        cpu_percent=h.cpu_percent,
        mem_percent=h.mem_percent,
        healthiness=health,
    )


@router.post(
    "/",
    response_model=HostRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],  # admin-only
)
async def register_host(
    req: HostCreate,
    db: AsyncSession = Depends(get_db),
):
    # 1) Create the host record
    new_host = ContainerHost(
        hostname=req.hostname,
        ip=str(req.ip),
        ssh_port=req.ssh_port,
        api_port=req.api_port,
        max_containers=req.max_containers,
        current_containers=0,
        status=HostStatus.offline,
        last_seen=None,
    )
    db.add(new_host)
    await db.flush()  # get new_host.id

    # 2) Issue a server key
    token = create_admin_token(str(new_host.id), exp_minutes=None)
    key = APIKey(
        owner_type=APIKeyOwner.server,
        owner_id=new_host.id,
        key_hash=hash_token(token),
        created_at=datetime.datetime.utcnow(),
        expires_at=None,
    )
    db.add(key)
    # 3) Link cred_ref to the APIKey record
    new_host.cred_ref = token

    await db.commit()

    return HostRegisterResponse(host_id=new_host.id, server_key=token)


@router.patch(
    "/{host_id}",
    response_model=HostInfo,
    dependencies=[Depends(get_current_admin)],  # admin-only
)
async def update_host(
    host_id: uuid.UUID,
    req: HostUpdate,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(ContainerHost).where(ContainerHost.id == host_id)
    res = await db.execute(stmt)
    h = res.scalar_one_or_none()
    if not h:
        raise HTTPException(status_code=404, detail="Host not found")

    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(h, field, value)
    await db.commit()
    await db.refresh(h)

    health = compute_healthiness(h.status, h.cpu_percent, h.mem_percent)
    return HostInfo(
        id=h.id,
        hostname=h.hostname,
        ip=h.ip,
        ssh_port=h.ssh_port,
        api_port=h.api_port,
        max_containers=h.max_containers,
        current_containers=h.current_containers,
        cpu_percent=h.cpu_percent,
        mem_percent=h.mem_percent,
        status=h.status,
        last_seen=h.last_seen,
        healthiness=health,
    )


@router.delete(
    "/{host_id}",
    dependencies=[Depends(get_current_admin)],  # admin-only
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_host(
    host_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    # 1) Revoke server keys for this host
    stmt_keys = select(APIKey).where(
        APIKey.owner_type == APIKeyOwner.server, APIKey.owner_id == host_id
    )
    res_keys = await db.execute(stmt_keys)
    for key in res_keys.scalars().all():
        key.expires_at = datetime.datetime.utcnow()

    # 2) Delete the host record
    stmt = select(ContainerHost).where(ContainerHost.id == host_id)
    res = await db.execute(stmt)
    host = res.scalar_one_or_none()
    if not host:
        raise HTTPException(status_code=404, detail="Host not found")

    await db.delete(host)
    await db.commit()
    return {"detail": "Host deleted successfully"}


@router.post(
    "/{host_id}/heartbeat",
    status_code=status.HTTP_200_OK,
    summary="Heartbeat from container host",
    dependencies=[Depends(get_server_key)],
)
async def host_heartbeat(
    host_id: uuid.UUID,
    payload: HeartbeatRequest,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(ContainerHost).where(ContainerHost.id == host_id)
    res = await db.execute(stmt)
    host = res.scalar_one_or_none()
    if not host:
        raise HTTPException(status_code=404, detail="Host not found")

    # Update host status
    host.current_containers = payload.containers
    host.cpu_percent = payload.cpu
    host.mem_percent = payload.mem
    host.last_seen = datetime.datetime.utcnow()
    host.status = HostStatus.healthy
    await db.commit()

    return {"ack": True}
