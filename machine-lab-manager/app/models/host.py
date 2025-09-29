import uuid
import datetime
import enum

from sqlalchemy import Column, String, Integer, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID, INET
from app.core.database import Base

class HostStatus(str, enum.Enum):
    healthy = "healthy"
    offline = "offline"

class ContainerHost(Base):
    __tablename__ = "container_hosts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    hostname = Column(
        String,
        nullable=False,
        doc="Logical name of the container server"
    )
    ip = Column(
        String,
        nullable=False,
        doc="Management IP of the host"
    )
    ssh_port = Column(
        Integer,
        default=22,
        nullable=False,
        doc="SSH port for admin access"
    )
    api_port = Column(
        Integer,
        default=8003,
        nullable=False,
        doc="Port the agent listens on for commands"
    )
    max_containers = Column(
        Integer,
        nullable=False,
        doc="Capacity limit of simultaneous containers"
    )
    current_containers = Column(
        Integer,
        default=0,
        nullable=False,
        doc="How many containers are currently running"
    )
    cpu_percent = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Last‐reported CPU usage %"
    )
    mem_percent = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Last‐reported RAM usage %"
    )
    status = Column(
        Enum(HostStatus),
        default=HostStatus.offline,
        nullable=False,
        doc="Last-known health status"
    )
    last_seen = Column(
        DateTime(timezone=True),
        default=datetime.datetime.utcnow,
        nullable=True,
        doc="Timestamp of most recent heartbeat"
    )
    cred_ref = Column(
        String,
        nullable=True,
        doc="X-Server-Key for agent authentication"
    )
