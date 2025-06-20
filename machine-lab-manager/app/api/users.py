import os
import glob
import subprocess
import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import VPNProfile
from app.api.deps import get_db, get_current_admin

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_admin)],  # admin-only
)

# ─── Request Schema ────────────────────────────────────────────────────
class CreateVPNReq(BaseModel):
    client_name: str

# ─── Constants & Helpers ────────────────────────────────────────────────
EASYRSA_DIR = "/etc/openvpn/easy-rsa"
PKI_DIR     = os.path.join(EASYRSA_DIR, "pki")
OVPN_DIR    = "/etc/openvpn/pki/ovpns"

def _run(cmd: list[str]) -> None:
    """Run an Easy-RSA command in the PKI dir."""
    subprocess.check_call(cmd, cwd=EASYRSA_DIR)

def _cleanup_artifacts(client: str):
    """
    Remove any leftover pki keys/certs and .ovpn bundles for this client.
    """
    patterns = [
        os.path.join(PKI_DIR, "issued",    f"{client}.*"),
        os.path.join(PKI_DIR, "private",   f"{client}.*"),
        os.path.join(OVPN_DIR,             f"{client}.ovpn"),
    ]
    for pat in patterns:
        for path in glob.glob(pat):
            try:
                os.remove(path)
            except OSError:
                pass

def _make_client(name: str) -> str:
    """
    1) Build client cert/key with Easy-RSA non-interactively
    2) Assemble an .ovpn by embedding CA, client cert/key, and ta.key
    """
    _run(["./easyrsa", "--batch", "build-client-full", name, "nopass"])

    # Read cert/key pieces
    ca   = open(os.path.join(PKI_DIR, "ca.crt"),   "r").read().strip()
    cert = open(os.path.join(PKI_DIR, "issued", f"{name}.crt"), "r").read().strip()
    key  = open(os.path.join(PKI_DIR, "private", f"{name}.key"),"r").read().strip()
    ta   = open(os.path.join(EASYRSA_DIR, "ta.key"),           "r").read().strip()

    # Build client config
    host  = os.getenv("OPENVPN_SERVER_HOST", "vpn.example.com")
    port  = os.getenv("OPENVPN_SERVER_PORT", "1194")
    proto = os.getenv("OPENVPN_PROTO", "udp")
    dev   = os.getenv("OPENVPN_DEV",   "tun")

    conf = [
        "client",
        f"dev {dev}",
        f"proto {proto}",
        f"remote {host} {port}",
        "resolv-retry infinite",
        "nobind",
        "persist-key",
        "persist-tun",
        "remote-cert-tls server",
        "<ca>",   ca,   "</ca>",
        "<cert>", cert, "</cert>",
        "<key>",  key,  "</key>",
        "key-direction 1",
        "<tls-auth>", ta, "</tls-auth>",
        "verb 3",
    ]

    os.makedirs(OVPN_DIR, exist_ok=True)
    out_path = os.path.join(OVPN_DIR, f"{name}.ovpn")
    with open(out_path, "w") as f:
        f.write("\n".join(conf) + "\n")

    return out_path

# ─── Endpoints ─────────────────────────────────────────────────────────

@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get existing or create a VPN profile for a client_name",
)
async def create_vpn_profile(
    req: CreateVPNReq,
    db: AsyncSession = Depends(get_db),
):
    client = req.client_name

    # 1) If there’s already an active profile, return it immediately
    stmt = select(VPNProfile).where(
        VPNProfile.client_name == client,
        VPNProfile.revoked == False
    )
    res = await db.execute(stmt)
    existing = res.scalar_one_or_none()
    if existing:
        return FileResponse(
            existing.config_path,
            media_type="application/x-openvpn-profile",
            filename=f"{client}.ovpn",
        )

    # 2) Otherwise clean up any stray files, generate new profile
    _cleanup_artifacts(client)
    ovpn_path = _make_client(client)

    # 3) Persist & return
    profile = VPNProfile(
        client_name=client,
        config_path=ovpn_path,
        revoked=False,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)

    return FileResponse(
        ovpn_path,
        media_type="application/x-openvpn-profile",
        filename=f"{client}.ovpn",
    )


@router.post(
    "/{client_name}/rotate-vpn",
    status_code=status.HTTP_200_OK,
    summary="Revoke old & issue a fresh VPN profile",
)
async def rotate_vpn_profile(
    client_name: str,
    db: AsyncSession = Depends(get_db),
):
    # 1) Revoke existing
    stmt = select(VPNProfile).where(
        VPNProfile.client_name == client_name,
        VPNProfile.revoked == False
    )
    res = await db.execute(stmt)
    for prof in res.scalars().all():
        prof.revoked = True

    # 2) Cleanup + generate fresh
    _cleanup_artifacts(client_name)
    ovpn_path = _make_client(client_name)

    # 3) Persist & return
    profile = VPNProfile(
        client_name=client_name,
        config_path=ovpn_path,
        revoked=False,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)

    return FileResponse(
        ovpn_path,
        media_type="application/x-openvpn-profile",
        filename=f"{client_name}.ovpn",
    )
