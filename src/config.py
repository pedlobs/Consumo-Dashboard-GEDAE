"""Centralized application settings, loaded from .env."""
from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the electricity consumption dashboard.

    Parameters

    database_url : str
        SQLAlchemy connection URL for the consumption readings database.
        Defaults to a local SQLite file. Can become a PostgreSQL URL
        with no code change .
    data_dir : Pat
        Directory containing the raw CSV files exported by the meters.
    consumer_unit_mapping_path : Path
        Path to a local JSON file mapping each real identifier (CSV file
        name) to a stable anonymized identifier. 
    log_level : str
        Minimum log level to display/record.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    database_url: str = Field(default="sqlite:///consumption.db")
    data_dir: Path = Field(default=Path("data"))
    consumer_unit_mapping_path: Path = Field(
        default=Path("consumer_unit_mapping.json")
    )
    log_level: str = Field(default="INFO")


settings = Settings()
