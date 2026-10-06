from abc import ABC, abstractmethod


class S3StorageServiceInterface(ABC):
    """Interface for asynchronous S3-compatible object storage operations."""

    @abstractmethod
    async def upload_bytes(
        self,
        bucket: str,
        key: str,
        data: bytes,
        content_type: str,
    ) -> str:
        """Upload raw binary data to the specified S3 bucket and key."""
        ...

    @abstractmethod
    async def generate_presigned_url(
        self,
        bucket: str,
        key: str,
        expires_in: int | None = None,
        http_method: str = "get_object",
    ) -> str:
        """Generate a presigned URL using S3_PUBLIC_ENDPOINT_URL for client-facing access."""
        ...

    @abstractmethod
    async def delete_file(self, bucket: str, key: str) -> None:
        """Delete an object from the specified S3 bucket."""
        ...

    @abstractmethod
    async def get_bytes(self, bucket: str, key: str) -> bytes:
        """Download and return raw bytes of an object from the specified S3 bucket."""
        ...

    @abstractmethod
    async def object_exists(self, bucket: str, key: str) -> bool:
        """Check whether an object exists in the specified S3 bucket."""
        ...
