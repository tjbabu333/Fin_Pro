from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = ""
    cors_origins: str = "http://localhost:5173"
    environment: str = "development"
    max_request_size_mb: int = 2

    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30
    db_pool_recycle: int = 300

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
