import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import engine, Base, SessionLocal
from app.models import User, UserRole
from app.core.security import hash_password
from app.core.config import get_settings
import datetime

async def init_models():
    async with engine.begin() as conn:
        # create tables
        await conn.run_sync(Base.metadata.create_all)

async def create_default_admin():
    settings = get_settings()
    async with SessionLocal() as session:
        stmt = select(User).where(User.email == settings.admin_default_email)
        result = await session.execute(stmt)
        admin = result.scalar_one_or_none()
        if admin:
            return
        new_admin = User(
            email=settings.admin_default_email,
            username="admin",
            password_hash=hash_password(settings.admin_default_password),
            role=UserRole.admin
        )
        session.add(new_admin)
        await session.commit()

async def monitor_offline_hosts():
    """
    Periodically scan all hosts: if last_seen > 30s ago, mark offline.
    """
    from sqlalchemy.future import select
    from app.core.database import SessionLocal
    from app.models import ContainerHost, HostStatus

    THRESHOLD = 30  # seconds
    while True:
        async with SessionLocal() as session:
            stmt = select(ContainerHost)
            res = await session.execute(stmt)
            hosts = res.scalars().all()
            now = datetime.datetime.utcnow()
            for host in hosts:
                if not host.last_seen or (now - host.last_seen).total_seconds() > THRESHOLD:
                    if host.status != HostStatus.offline:
                        host.status = HostStatus.offline
            await session.commit()
        await asyncio.sleep(THRESHOLD)


async def startup():
    await init_models()
    await create_default_admin()
    asyncio.create_task(monitor_offline_hosts())
