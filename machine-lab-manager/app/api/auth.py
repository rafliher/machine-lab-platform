from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import datetime

from app.core.database import SessionLocal
from app.models import User, UserRole, APIKey, APIKeyOwner
from app.core.security import (
    verify_password,
    hash_token,
    create_admin_token,
    hash_password,
)
from app.api.deps import get_db, get_current_admin

router = APIRouter(prefix="/auth", tags=["auth"])


# --------------------
# LOGIN (unchanged)
# --------------------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    admin_key: str
    expires: datetime.datetime | None = None  # timeless keys yield null


@router.post(
    "/login", 
    response_model=LoginResponse,
    summary="Admin login",
    description="Authenticate as admin and receive an API key for subsequent requests."
)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Login as an administrator and receive an API key.
    
    The returned admin_key should be included in the `X-Admin-Key` header 
    for authenticated requests to other endpoints.
    """
    stmt = select(User).where(User.email == req.email, User.role == UserRole.admin)
    res = await db.execute(stmt)
    user: User | None = res.scalar_one_or_none()

    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_admin_token(str(user.id), exp_minutes=None)  # no expiry
    api_key = APIKey(
        owner_type=APIKeyOwner.admin,
        owner_id=user.id,
        key_hash=hash_token(token),
        expires_at=None,
    )
    db.add(api_key)
    await db.commit()

    return LoginResponse(admin_key=token, expires=None)


# --------------------
# CHANGE PASSWORD
# --------------------
class PWChangeReq(BaseModel):
    current_password: str
    new_password: str


class MessageResponse(BaseModel):
    message: str


@router.post(
    "/change-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Change admin password",
    description="Change the current admin user's password."
)
async def change_password(
    body: PWChangeReq,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Change the password for the currently authenticated admin user.
    
    Requires the current password for verification.
    """
    if not verify_password(body.current_password, admin.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong current password")

    admin.password_hash = hash_password(body.new_password)
    await db.commit()
    return MessageResponse(message="Password changed successfully")


# --------------------
# ROTATE ADMIN KEY
# --------------------
class RotateKeyResponse(BaseModel):
    message: str
    admin_key: str


@router.post(
    "/rotate-key",
    response_model=RotateKeyResponse,
    status_code=status.HTTP_200_OK,
    summary="Rotate admin API key",
    description="Revoke current API key and issue a new one."
)
async def rotate_key(
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Rotate the admin API key.
    
    This will:
    1. Revoke all existing API keys for the admin
    2. Issue a new API key
    3. Return the new key
    
    Update your client to use the new admin_key for future requests.
    """
    # Revoke existing keys
    now = datetime.datetime.utcnow()
    stmt = select(APIKey).where(APIKey.owner_id == admin.id)
    res = await db.execute(stmt)
    for key in res.scalars():
        key.expires_at = now

    # Issue new limitless key
    token = create_admin_token(str(admin.id), exp_minutes=None)
    new_key = APIKey(
        owner_type=APIKeyOwner.admin,
        owner_id=admin.id,
        key_hash=hash_token(token),
        expires_at=None,
    )
    db.add(new_key)
    await db.commit()

    return RotateKeyResponse(
        message="Admin key rotated successfully",
        admin_key=token
    )
