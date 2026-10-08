from abc import ABC, abstractmethod
from typing import Sequence

from fastapi import UploadFile

from schemas.media import UploadedMediaOut


class MediaServiceInterface(ABC):
    """Interface for processing, uploading, caching, and serving media objects."""

    @abstractmethod
    def build_file_key(self, entity_type: str, entity_id: int, extension: str = "webp") -> str:
        """Generate unique storage key following private/{entity_type}/{entity_id}/{uuid}.{ext} pattern."""
        ...

    @abstractmethod
    def build_cache_key(self, user_id: int, file_key: str) -> str:
        """Format presigned URL cache key following presigned:{user_id}:{file_key} convention."""
        ...

    @abstractmethod
    async def upload_media(
        self,
        file: UploadFile,
        entity_type: str,
        entity_id: int,
        user_id: int,
        max_size_bytes: int | None = None,
        max_dimension: int | None = None,
    ) -> UploadedMediaOut:
        """Validate uploaded file, normalize to WebP, store in S3, and cache presigned URL."""
        ...

    @abstractmethod
    async def get_presigned_url(self, user_id: int, file_key: str) -> str:
        """Retrieve presigned URL from cache or generate a new S3 URL and cache it."""
        ...

    @abstractmethod
    async def get_presigned_urls(
        self, user_id: int, file_keys: Sequence[str]
    ) -> dict[str, str]:
        """Batch retrieve presigned URLs from cache or S3 for multiple file keys."""
        ...

    @abstractmethod
    async def delete_media(self, user_id: int, file_key: str) -> None:
        """Delete media object from S3 storage and invalidate its cached presigned URL."""
        ...

