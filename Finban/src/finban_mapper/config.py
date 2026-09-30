"""Environment-driven settings."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="FINBAN_")

    database_url: str = "postgresql+psycopg2://finban:finban@localhost:5432/finban_mapper"
    lexware_office_api_key: str = "changeme"
    mapping_rules_path: str = str(
        Path(__file__).parent / "mapping" / "seed_rules.yaml"
    )


settings = Settings()
