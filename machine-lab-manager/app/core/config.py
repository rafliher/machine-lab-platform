import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Database
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., env="POSTGRES_DB")
    postgres_host: str = Field(default="db", env="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, env="POSTGRES_PORT")

    # Auth
    jwt_secret: str = Field(..., env="JWT_SECRET")
    admin_default_email: str = Field(..., env="ADMIN_DEFAULT_EMAIL")
    admin_default_password: str = Field(..., env="ADMIN_DEFAULT_PASSWORD")

    @property
    def database_uri(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        case_sensitive = False

@lru_cache
def get_settings():
    return Settings()