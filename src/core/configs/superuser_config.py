from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SuperUserConfig(BaseSettings):
    SUPERUSER_USERNAME: str = Field(
        min_length=3,
        max_length=50,
        description="Initial superuser username",
    )
    SUPERUSER_EMAIL: EmailStr = Field(
        description="Initial superuser email",
    )
    SUPERUSER_PASSWORD: str = Field(
        min_length=8,
        description="Initial superuser password",
    )

    model_config = SettingsConfigDict(
        env_prefix="FIRST_",
        extra="ignore",
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
    )


superuser_config = SuperUserConfig()  # type: ignore[call-arg]