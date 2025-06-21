import uuid
import datetime
import enum

from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base

class ContainerStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    stopped = "stopped"
    error = "error"

class Container(Base):
    __tablename__ = "containers"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        doc="Unique container identifier",
    )
    user_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        doc="Owner user",
    )
    host_id = Column(
        UUID(as_uuid=True),
        ForeignKey("container_hosts.id", ondelete="CASCADE"),
        nullable=False,
        doc="Which host is running this container",
    )
    name = Column(
        String,
        nullable=False,
        doc="Logical name (and Docker container name)",
    )
    status = Column(
        Enum(ContainerStatus, name="containerstatus"),
        nullable=False,
        default=ContainerStatus.pending,
        doc="Current lifecycle state",
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        doc="When this request was first created",
    )
