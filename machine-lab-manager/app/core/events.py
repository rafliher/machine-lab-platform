import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import engine, Base, SessionLocal
from app.models import User, UserRole
from app.core.security import hash_password
from app.core.config import get_settings

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

async def startup():
    await init_models()
    await create_default_admin()
