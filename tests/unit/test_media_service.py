from unittest.mock import AsyncMock, MagicMock
import pytest
from fastapi import UploadFile

from schemas.image import ValidatedImage
from services.media_service import MediaConfig, MediaService


@pytest.fixture
def mock_image_validator() -> AsyncMock:
    validator = AsyncMock()
    validator.validate_and_process.return_value = ValidatedImage(
        content=b"webp-image-bytes",
        content_type="image/webp",
        format="WEBP",
        width=800,
        height=600,
        size_bytes=len(b"webp-image-bytes"),
        original_filename="sample.jpg",
    )
    return validator


@pytest.fixture
def mock_storage_service() -> AsyncMock:
    storage = AsyncMock()
    storage.upload_bytes.return_value = "file_key"
    storage.generate_presigned_url.return_value = (
        "http://localhost:8333/media/test.webp?sig=123"
    )
    storage.delete_file.return_value = None
    return storage


@pytest.fixture
def mock_cache_service() -> AsyncMock:
    cache = AsyncMock()
    cache.get.return_value = None
    cache.set.return_value = True
    cache.delete.return_value = True
    return cache


@pytest.fixture
def media_service(
    mock_image_validator: AsyncMock,
    mock_storage_service: AsyncMock,
    mock_cache_service: AsyncMock,
) -> MediaService:
    config = MediaConfig(
        bucket_name="media",
        s3_presigned_ttl_seconds=7200,
        cache_url_ttl_seconds=3600,
    )
    return MediaService(
        image_validator=mock_image_validator,
        storage_service=mock_storage_service,
        cache_service=mock_cache_service,
        config=config,
    )


def test_build_file_key(media_service: MediaService):
    key = media_service.build_file_key(entity_type="garments", entity_id=42)
    assert key.startswith("private/garments/42/")
    assert key.endswith(".webp")


def test_build_cache_key(media_service: MediaService):
    cache_key = media_service.build_cache_key(
        user_id=1, file_key="private/garments/42/abc.webp"
    )
    assert cache_key == "presigned:1:private/garments/42/abc.webp"


@pytest.mark.asyncio
async def test_upload_media_success(
    media_service: MediaService,
    mock_image_validator: AsyncMock,
    mock_storage_service: AsyncMock,
    mock_cache_service: AsyncMock,
):
    fake_upload_file = MagicMock(spec=UploadFile)
    fake_upload_file.filename = "test.png"

    result = await media_service.upload_media(
        file=fake_upload_file,
        entity_type="garments",
        entity_id=15,
        user_id=3,
    )

    mock_image_validator.validate_and_process.assert_awaited_once_with(
        file=fake_upload_file,
        max_size_bytes=None,
        max_dimension=None,
    )

    assert result.file_key.startswith("private/garments/15/")
    assert result.file_key.endswith(".webp")
    assert result.url == "http://localhost:8333/media/test.webp?sig=123"
    assert result.width == 800
    assert result.height == 600

    mock_storage_service.upload_bytes.assert_awaited_once_with(
        bucket="media",
        key=result.file_key,
        data=b"webp-image-bytes",
        content_type="image/webp",
    )

    mock_storage_service.generate_presigned_url.assert_awaited_once_with(
        bucket="media",
        key=result.file_key,
        expires_in=7200,
    )

    expected_cache_key = f"presigned:3:{result.file_key}"
    mock_cache_service.set.assert_awaited_once_with(
        key=expected_cache_key,
        value="http://localhost:8333/media/test.webp?sig=123",
        ttl=3600,
    )


@pytest.mark.asyncio
async def test_get_presigned_url_cache_hit(
    media_service: MediaService,
    mock_storage_service: AsyncMock,
    mock_cache_service: AsyncMock,
):
    file_key = "private/garments/10/xyz.webp"
    cached_url = "http://cached-url.example/test.webp"
    mock_cache_service.get.return_value = cached_url

    url = await media_service.get_presigned_url(user_id=7, file_key=file_key)

    assert url == cached_url
    mock_cache_service.get.assert_awaited_once_with(f"presigned:7:{file_key}")
    mock_storage_service.generate_presigned_url.assert_not_called()


@pytest.mark.asyncio
async def test_get_presigned_url_cache_miss(
    media_service: MediaService,
    mock_storage_service: AsyncMock,
    mock_cache_service: AsyncMock,
):
    file_key = "private/garments/10/xyz.webp"
    fresh_url = "http://fresh-s3-url.example/test.webp"
    mock_cache_service.get.return_value = None
    mock_storage_service.generate_presigned_url.return_value = fresh_url

    url = await media_service.get_presigned_url(user_id=7, file_key=file_key)

    assert url == fresh_url
    mock_cache_service.get.assert_awaited_once_with(f"presigned:7:{file_key}")
    mock_storage_service.generate_presigned_url.assert_awaited_once_with(
        bucket="media",
        key=file_key,
        expires_in=7200,
    )
    mock_cache_service.set.assert_awaited_once_with(
        key=f"presigned:7:{file_key}",
        value=fresh_url,
        ttl=3600,
    )


@pytest.mark.asyncio
async def test_delete_media(
    media_service: MediaService,
    mock_storage_service: AsyncMock,
    mock_cache_service: AsyncMock,
):
    file_key = "private/garments/10/xyz.webp"

    await media_service.delete_media(user_id=7, file_key=file_key)

    mock_storage_service.delete_file.assert_awaited_once_with(
        bucket="media",
        key=file_key,
    )
    mock_cache_service.delete.assert_awaited_once_with(f"presigned:7:{file_key}")

