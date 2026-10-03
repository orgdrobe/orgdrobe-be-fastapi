from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class S3Config(BaseSettings):
    ENDPOINT_URL: AnyHttpUrl = Field(
        description="Internal S3 endpoint URL for backend (e.g. http://seaweedfs-s3:8333)",
    )
    PUBLIC_ENDPOINT_URL: AnyHttpUrl = Field(
        description="Public S3 endpoint URL for client signatures (e.g. https://s3.example.com or http://localhost:8333)",
    )
    ACCESS_KEY: str = Field(
        default="any_key",
        min_length=1,
        description="S3 access key",
    )
    SECRET_KEY: str = Field(
        default="any_secret",
        min_length=1,
        description="S3 secret key",
    )
    BUCKET_NAME: str = Field(
        default="media",
        min_length=3,
        max_length=63,
        description="Default S3 bucket name",
    )
    PRESIGNED_URL_TTL_SECONDS: int = Field(
        default=7200,
        gt=0,
        le=604800,
        description="TTL for presigned URLs in seconds (default: 7200 - 2 hours)",
    )

    model_config = SettingsConfigDict(
        env_prefix="S3_",
        extra="ignore",
        env_file=(".env"),
        env_file_encoding="utf-8",
    )


s3_config = S3Config()  # type: ignore[call-arg]