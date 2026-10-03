from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .base import ENV_FILE

class DatabaseConfig(BaseSettings):
    DIALECT_DRIVER: str = Field(
        default="postgresql+asyncpg",
        min_length=1,
        description="Database dialect and driver (e.g. postgresql+asyncpg)",
    )
    USERNAME: str = Field(
        default="admin",
        min_length=1,
        description="Database username",
    )
    PASSWORD: str = Field(
        default="mypassword",
        description="Database password",
    )
    HOST: str = Field(
        default="localhost",
        min_length=1,
        description="Database host",
    )
    PORT: int = Field(
        default=5432,
        ge=1,
        le=65535,
        description="Database port",
    )
    NAME_OR_PATH: str = Field(
        default="admin",
        min_length=1,
        description="Database name or path",
    )
    SHOW_LOGGING: bool = Field(
        default=False,
        description="Show SQL query logs",
    )

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        extra="ignore",
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )


database_config = DatabaseConfig()  # type: ignore[call-arg]