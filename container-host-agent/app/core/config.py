import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    jwt_secret: str = Field(..., env="JWT_SECRET")
    docker_socket: str = Field("unix:///var/run/docker.sock", env="DOCKER_SOCKET")

    # heartbeat
    manager_url: str = Field(..., env="MANAGER_URL")
    host_id: str      = Field(..., env="HOST_ID")
    server_key: str   = Field(..., env="SERVER_KEY")
    heartbeat_interval: int = Field(10, env="HEARTBEAT_INTERVAL")

    class Config:
        case_sensitive = False

settings = Settings()
