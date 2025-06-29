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
    summary="Get existing or create a VPN profile for a client_name",
    status_code=status.HTTP_200_OK,
)
async def create_vpn_profile(
    req: CreateVPNReq,
    db: AsyncSession = Depends(get_db),
):
    """
    Creates (or returns) a WireGuard/OpenVPN profile for `client_name`,
    assigning a static IP if new.
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
    summary="Revoke old & issue a fresh VPN profile",
    status_code=status.HTTP_200_OK,
)
async def rotate_vpn_profile(
    client_name: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Revokes any existing profile for `client_name` (clears iptables, DB flag, files),
    then issues a brand-new .ovpn with a new static IP.
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
