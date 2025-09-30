import uuid
import datetime
from sqlalchemy import Column, Text, Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID, INET
from app.core.database import Base

class VPNProfile(Base):
    __tablename__ = "vpn_profiles"

    # Primary key for the profile record
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        doc="Unique VPN profile ID",
    )

    # Logical VPN username or lab‐user identifier
    client_name = Column(
        String,
        nullable=False,
        index=True,
        doc="Client identifier for this profile",
    )

    # Assigned VPN IP address
    ip_address = Column(
        INET,
        nullable=False,
        unique=False,
        doc="Static VPN IP assigned to this client",
    )

    # Path on disk where the .ovpn file lives
    config_path = Column(
        Text,
        nullable=False,
        doc="Filesystem path to the generated .ovpn",
    )

    # Has this profile been revoked/rotated?
    revoked = Column(
        Boolean,
        nullable=False,
        default=False,
        doc="True once this profile has been rotated or revoked",
    )

    # When this profile was first generated
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.utcnow,
        doc="Timestamp of profile creation",
    )
