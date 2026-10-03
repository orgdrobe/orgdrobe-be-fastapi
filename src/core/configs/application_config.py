from typing import Literal

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationConfig(BaseSettings):
    PORT: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="Application server port",
    )
    ENV: Literal["DEV", "PROD", "STAGE", "TEST"] = Field(
        default="DEV",
        description="Application environment (DEV, PROD, STAGE, TEST)",
    )
    FRONTEND_URL: AnyHttpUrl = Field(
        default="http://localhost:3000",
        description="Frontend application URL",
    )

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        extra="ignore",
        env_file=(".env"),
        env_file_encoding="utf-8",
    )


application_config = ApplicationConfig()  # type: ignore[call-arg]