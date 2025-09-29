# app/api/users.py
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_db, get_current_admin
from app.models import VPNProfile
from app.internal.vpn import (
    create_or_get_profile,
    remove_vpn_profile,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_admin)],  # admin-only
)

# ─── Request Schema ────────────────────────────────────────────────────

class CreateVPNReq(BaseModel):
    client_name: str


# ─── Endpoints ─────────────────────────────────────────────────────────

@router.post(
    "/vpn",
    summary="Create or get VPN profile",
    description="Create a new VPN profile for a client or return existing one if already exists.",
    status_code=status.HTTP_200_OK,
)
async def create_vpn_profile(
    req: CreateVPNReq,
    db: AsyncSession = Depends(get_db),
):
    """
    Creates or returns a VPN profile for the specified client.
    
    If a profile already exists for the client_name, returns the existing profile.
    If not, creates a new OpenVPN profile with a static IP assignment.
    
    The returned file is an .ovpn configuration file that can be imported
    into OpenVPN clients for secure access to containerized environments.
    """
    print(f"Creating VPN profile for {req.client_name}")
    path = await create_or_get_profile(db, req.client_name)
    return FileResponse(
        path,
        media_type="application/x-openvpn-profile",
        filename=f"{req.client_name}.ovpn",
    )


@router.post(
    "/vpn/{client_name}/rotate",
    summary="Rotate VPN profile",
    description="Revoke existing VPN profile and create a new one with fresh credentials.",
    status_code=status.HTTP_200_OK,
)
async def rotate_vpn_profile(
    client_name: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Rotate the VPN profile for a specific client.
    
    This operation:
    1. Revokes any existing profile for the client
    2. Removes associated firewall rules and certificates
    3. Creates a brand-new VPN profile with fresh credentials
    4. Assigns a new static IP address
    
    Use this when a VPN profile may be compromised or needs to be renewed.
    """
    # Ensure there was something to revoke (optional)
    stmt = await db.execute(
        select(VPNProfile).where(
            VPNProfile.client_name == client_name,
            VPNProfile.revoked == False
        )
    )
    # if not stmt.scalars().first():
    #     raise HTTPException(
    #         status_code=404,
    #         detail=f"No active VPN profile for '{client_name}' to rotate"
    #     )

    # Tear down existing profile + firewall rules
    await remove_vpn_profile(db, client_name)

    # Create fresh profile
    path = await create_or_get_profile(db, client_name)
    return FileResponse(
        path,
        media_type="application/x-openvpn-profile",
        filename=f"{client_name}.ovpn",
    )
