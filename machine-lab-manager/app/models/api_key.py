from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid, datetime
from app.core.database import Base
import enum

class APIKeyOwner(str, enum.Enum):
    admin = "admin"
    server = "server"

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_type = Column(Enum(APIKeyOwner), nullable=False)
    owner_id = Column(UUID(as_uuid=True), nullable=True, index=True, doc="References users.id when owner_type=admin, container_hosts.id when server")
    key_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
