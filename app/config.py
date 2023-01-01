from functools import lru_cache
from typing import List

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # https://docs.pydantic.dev/usage/settings
    db_host: str = Field("localhost")
    db_port: int = Field(5432)
    db_name: str = Field("sakuva")
    db_username: str
    db_password: str

    es_host: str
    es_index: str

    # Absolute path to data dir where images etc. are stored
    media_dir: str

    thumbnail_sizes: List[int] = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]

    api_key: str

    class Config:
        # https://docs.pydantic.dev/usage/settings/#dotenv-env-support
        # Environment variables will always take priority over values loaded from a dotenv file.
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """
    https://fastapi.tiangolo.com/advanced/settings/#creating-the-settings-only-once-with-lru_cache
    """
    return Settings()
