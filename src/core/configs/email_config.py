from pydantic import EmailStr, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class EmailConfig(BaseSettings):
    USERNAME: str = Field(
        default="",
        description="SMTP username",
    )
    PASSWORD: SecretStr = Field(
        default=SecretStr(""),
        description="SMTP password",
    )
    FROM: EmailStr = Field(
        default="noreply@example.com",
        description="Sender email address",
    )
    PORT: int = Field(
        default=587,
        ge=1,
        le=65535,
        description="SMTP server port",
    )
    SERVER: str = Field(
        default="smtp.gmail.com",
        min_length=1,
        description="SMTP server host",
    )
    FROM_NAME: str = Field(
        default="SmartWardrobe",
        min_length=1,
        description="Sender display name",
    )

    model_config = SettingsConfigDict(
        env_prefix="MAIL_",
        extra="ignore",
        env_file=(".env"),
        env_file_encoding="utf-8",
    )


email_config = EmailConfig()  # type: ignore[call-arg]