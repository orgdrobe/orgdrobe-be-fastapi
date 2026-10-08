from fastapi import Depends

from services import MediaService
from services.interfaces import (
    CacheServiceInterface,
    ImageValidatorServiceInterface,
    MediaServiceInterface,
    S3StorageServiceInterface,
)
from .cache_service import get_cache_service
from .image_validator_service import get_image_validator_service
from .s3_storage_service import get_s3_storage_service


def get_media_service(
    image_validator: ImageValidatorServiceInterface = Depends(
        get_image_validator_service
    ),
    storage_service: S3StorageServiceInterface = Depends(
        get_s3_storage_service
    ),
    cache_service: CacheServiceInterface = Depends(get_cache_service),
) -> MediaServiceInterface:
    """Provide MediaService instance with image validator, S3 storage, and cache dependencies."""
    return MediaService(
        image_validator=image_validator,
        storage_service=storage_service,
        cache_service=cache_service,
    )

