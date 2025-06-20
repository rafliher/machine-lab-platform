import uuid
import datetime
from sqlalchemy import Column, Text, Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class VPNProfile(Base):
    __tablename__ = "vpn_profiles"

    # Primary key for the profile record
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # Name of the VPN client (not tied to your admin users)
    client_name = Column(
        String,
        nullable=False,
        index=True,
        doc="Logical VPN username or lab‐user identifier"
    )

    # Path on disk where the .ovpn file lives
    config_path = Column(
        Text,
        nullable=False,
        doc="Filesystem path to the generated .ovpn"
    )

    # Has this profile been revoked/rotated?
    revoked = Column(
        Boolean,
        nullable=False,
        default=False,
        doc="True once this profile has been rotated or revoked"
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.utcnow,
        doc="When this profile was first generated"
    )
