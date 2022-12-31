from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # https://docs.pydantic.dev/usage/settings
    db_host: str = Field("localhost")
    db_port: int = Field(5432)
    db_name: str = Field("sakuva")
    db_username: str
    db_password: str

    # Absolute path to data dir where images etc. are stored
    media_dir: str

    api_key: str

    class Config:
        # https://docs.pydantic.dev/usage/settings/#dotenv-env-support
        # Environment variables will always take priority over values loaded from a dotenv file.
        env_file = ".env"
