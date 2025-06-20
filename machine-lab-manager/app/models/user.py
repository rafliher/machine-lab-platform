from sqlalchemy import Column, String, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"

class UserState(str, enum.Enum):
    active = "active"
    suspended = "suspended"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    state = Column(Enum(UserState), default=UserState.active, nullable=False)
