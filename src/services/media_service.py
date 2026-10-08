from dataclasses import dataclass, field
from typing import Sequence
from uuid import uuid4

from fastapi import UploadFile
import structlog

from core.configs import s3_config
from schemas.media import UploadedMediaOut
from services.interfaces.cache_service_interface import CacheServiceInterface
from services.interfaces.image_validator_service_interface import (
    ImageValidatorServiceInterface,
)
from services.interfaces.media_service_interface import MediaServiceInterface
from services.interfaces.s3_storage_service_interface import (
    S3StorageServiceInterface,
)

logger = structlog.get_logger()


@dataclass
class MediaConfig:
    """Configuration settings for media processing, storage, and caching."""

    bucket_name: str = field(default_factory=lambda: s3_config.BUCKET_NAME)
    s3_presigned_ttl_seconds: int = field(
        default_factory=lambda: s3_config.PRESIGNED_URL_TTL_SECONDS
    )  # default: 7200 (2 hours)
    cache_url_ttl_seconds: int = 3600  # 1 hour


class MediaService(MediaServiceInterface):
    def __init__(
        self,
        image_validator: ImageValidatorServiceInterface,
        storage_service: S3StorageServiceInterface,
        cache_service: CacheServiceInterface,
        config: MediaConfig | None = None,
    ) -> None:
        self._image_validator = image_validator
        self._storage_service = storage_service
        self._cache_service = cache_service
        self.config = config or MediaConfig()

    def build_file_key(
        self, entity_type: str, entity_id: int, extension: str = "webp"
    ) -> str:
        """Generate unique storage key following private/{entity_type}/{entity_id}/{uuid}.{ext} pattern."""
        uuid_str = uuid4().hex
        ext = extension.lstrip(".")
        return f"private/{entity_type}/{entity_id}/{uuid_str}.{ext}"

    def build_cache_key(self, user_id: int, file_key: str) -> str:
        """Format presigned URL cache key following presigned:{user_id}:{file_key} convention."""
        return f"presigned:{user_id}:{file_key}"

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
        logger.info(
            "media_upload_started",
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            filename=file.filename,
        )

        validated = await self._image_validator.validate_and_process(
            file=file,
            max_size_bytes=max_size_bytes,
            max_dimension=max_dimension,
        )

        file_key = self.build_file_key(
            entity_type=entity_type,
            entity_id=entity_id,
            extension="webp",
        )

        await self._storage_service.upload_bytes(
            bucket=self.config.bucket_name,
            key=file_key,
            data=validated.content,
            content_type=validated.content_type,
        )

        url = await self._storage_service.generate_presigned_url(
            bucket=self.config.bucket_name,
            key=file_key,
            expires_in=self.config.s3_presigned_ttl_seconds,
        )

        cache_key = self.build_cache_key(user_id=user_id, file_key=file_key)
        await self._cache_service.set(
            key=cache_key,
            value=url,
            ttl=self.config.cache_url_ttl_seconds,
        )

        logger.info(
            "media_uploaded_and_cached",
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            file_key=file_key,
            width=validated.width,
            height=validated.height,
        )

        return UploadedMediaOut(
            file_key=file_key,
            url=url,
            width=validated.width,
            height=validated.height,
            size_bytes=validated.size_bytes,
        )

    async def get_presigned_url(self, user_id: int, file_key: str) -> str:
        """Retrieve presigned URL from cache or generate a new S3 URL and cache it."""
        cache_key = self.build_cache_key(user_id=user_id, file_key=file_key)
        cached_url = await self._cache_service.get(cache_key)

        if cached_url:
            logger.debug(
                "presigned_url_cache_hit",
                user_id=user_id,
                file_key=file_key,
            )
            return str(cached_url)

        logger.debug(
            "presigned_url_cache_miss",
            user_id=user_id,
            file_key=file_key,
        )

        url = await self._storage_service.generate_presigned_url(
            bucket=self.config.bucket_name,
            key=file_key,
            expires_in=self.config.s3_presigned_ttl_seconds,
        )

        await self._cache_service.set(
            key=cache_key,
            value=url,
            ttl=self.config.cache_url_ttl_seconds,
        )

        return url

    async def get_presigned_urls(
        self, user_id: int, file_keys: Sequence[str]
    ) -> dict[str, str]:
        """Batch retrieve presigned URLs from cache or S3 for multiple file keys."""
        urls: dict[str, str] = {}
        for key in file_keys:
            urls[key] = await self.get_presigned_url(user_id=user_id, file_key=key)
        return urls

    async def delete_media(self, user_id: int, file_key: str) -> None:
        """Delete media object from S3 storage and invalidate its cached presigned URL."""
        logger.info(
            "media_deletion_requested",
            user_id=user_id,
            file_key=file_key,
        )
        await self._storage_service.delete_file(
            bucket=self.config.bucket_name,
            key=file_key,
        )
        cache_key = self.build_cache_key(user_id=user_id, file_key=file_key)
        await self._cache_service.delete(cache_key)
        logger.info(
            "media_deleted_and_cache_invalidated",
            user_id=user_id,
            file_key=file_key,
        )

