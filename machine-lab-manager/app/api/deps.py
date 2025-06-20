from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import jwt

from app.core.config import get_settings
from app.core.security import hash_token
from app.core.database import SessionLocal
from app.models import User, UserRole, APIKey

settings = get_settings()


async def get_db():
    async with SessionLocal() as sess:
        yield sess


async def get_current_admin(
    x_admin_key: str = Header(..., alias="X-Admin-Key"),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(
            x_admin_key,
            settings.jwt_secret,
            algorithms=["HS256"],
            options={"verify_exp": False},  # we allow timeless tokens
        )
        user_id = payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad token")

    # Is token hash present & not revoked/expired?
    stmt = select(APIKey).where(APIKey.key_hash == hash_token(x_admin_key))
    res = await db.execute(stmt)
    if not res.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Key revoked")

    # Load user
    stmt = select(User).where(User.id == user_id, User.role == UserRole.admin)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No such admin")

    return user
