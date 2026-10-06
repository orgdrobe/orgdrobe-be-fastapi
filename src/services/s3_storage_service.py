from dataclasses import dataclass, field

import aioboto3
from botocore.config import Config
from botocore.exceptions import ClientError
from pydantic import AnyHttpUrl

from core.configs import s3_config
from core.exceptions.s3_exceptions import S3ObjectNotFound
from services.interfaces.s3_storage_service_interface import (
    S3StorageServiceInterface,
)


@dataclass
class S3ConnectionConfig:
    """Configuration parameters for S3 client connections with fallback to s3_config."""

    endpoint_url: str = field(
        default_factory=lambda: str(s3_config.ENDPOINT_URL).rstrip("/")
    )
    public_endpoint_url: str = field(
        default_factory=lambda: str(s3_config.PUBLIC_ENDPOINT_URL).rstrip("/")
    )
    access_key: str = field(default_factory=lambda: s3_config.ACCESS_KEY)
    secret_key: str = field(default_factory=lambda: s3_config.SECRET_KEY)
    default_bucket: str = field(default_factory=lambda: s3_config.BUCKET_NAME)
    default_ttl_seconds: int = field(
        default_factory=lambda: s3_config.PRESIGNED_URL_TTL_SECONDS
    )
    region_name: str = "us-east-1"

    def __post_init__(self) -> None:
        self.endpoint_url = str(self.endpoint_url).rstrip("/")
        self.public_endpoint_url = str(self.public_endpoint_url).rstrip("/")


class S3StorageService(S3StorageServiceInterface):
    def __init__(self, config: S3ConnectionConfig | None = None) -> None:
        self.config = config or S3ConnectionConfig()

        self._session = aioboto3.Session()
        self._s3_config = Config(
            signature_version="s3v4",
            s3={"addressing_style": "path"},
        )

    def _get_internal_client(self):
        """Client connected to the internal endpoint for backend data operations."""
        return self._session.client(
            "s3",
            endpoint_url=self.config.endpoint_url,
            aws_access_key_id=self.config.access_key,
            aws_secret_access_key=self.config.secret_key,
            region_name=self.config.region_name,
            config=self._s3_config,
        )

    def _get_public_client(self):
        """Client configured with public endpoint for generating client-accessible presigned URLs."""
        return self._session.client(
            "s3",
            endpoint_url=self.config.public_endpoint_url,
            aws_access_key_id=self.config.access_key,
            aws_secret_access_key=self.config.secret_key,
            region_name=self.config.region_name,
            config=self._s3_config,
        )

    async def upload_bytes(
        self,
        bucket: str,
        key: str,
        data: bytes,
        content_type: str,
    ) -> str:
        """Upload raw binary data to the specified S3 bucket and key."""
        async with self._get_internal_client() as s3_client:
            await s3_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=data,
                ContentType=content_type,
            )
            return key

    async def generate_presigned_url(
        self,
        bucket: str,
        key: str,
        expires_in: int | None = None,
        http_method: str = "get_object",
    ) -> str:
        """Generate a presigned URL using S3_PUBLIC_ENDPOINT_URL for client downloads/access."""
        ttl = expires_in if expires_in is not None else self.config.default_ttl_seconds
        async with self._get_public_client() as s3_client:
            url: str = await s3_client.generate_presigned_url(
                ClientMethod=http_method,
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=ttl,
            )
            return url

    async def delete_file(self, bucket: str, key: str) -> None:
        """Delete an object from the specified S3 bucket."""
        async with self._get_internal_client() as s3_client:
            await s3_client.delete_object(Bucket=bucket, Key=key)

    async def get_bytes(self, bucket: str, key: str) -> bytes:
        """Download and return raw bytes of an object from the specified S3 bucket."""
        try:
            async with self._get_internal_client() as s3_client:
                response = await s3_client.get_object(Bucket=bucket, Key=key)
                async with response["Body"] as stream:
                    content: bytes = await stream.read()
                    return content
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code")
            if error_code in ("NoSuchKey", "404"):
                raise S3ObjectNotFound(bucket=bucket, key=key) from exc
            raise

    async def object_exists(self, bucket: str, key: str) -> bool:
        """Check whether an object exists in the specified S3 bucket."""
        try:
            async with self._get_internal_client() as s3_client:
                await s3_client.head_object(Bucket=bucket, Key=key)
                return True
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code")
            if error_code in ("NoSuchKey", "404", "NotFound"):
                return False
            raise
