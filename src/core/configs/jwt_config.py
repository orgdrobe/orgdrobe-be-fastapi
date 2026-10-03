from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .base import ENV_FILE

class JwtConfig(BaseSettings):
    SECRET_KEY: str = Field(
        min_length=16,
        description="Secret key for JWT generation and verification",
    )
    ALGORITHM: Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"] = Field(
        default="HS256",
        description="JWT hashing algorithm",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=15,
        gt=0,
        description="Access token expiration in minutes",
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=30,
        gt=0,
        description="Refresh token expiration in days",
    )
    RESET_EMAIL_TOKEN_EXPIRE_MINUTES: int = Field(
        default=15,
        gt=0,
        description="Reset email token expiration in minutes",
    )

    model_config = SettingsConfigDict(
        env_prefix="SECURITY_",
        extra="ignore",
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )


jwt_config = JwtConfig()  # type: ignore[call-arg]