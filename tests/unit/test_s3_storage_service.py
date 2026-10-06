from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from botocore.exceptions import ClientError

from core.exceptions.s3_exceptions import S3ObjectNotFound
from services.s3_storage_service import S3ConnectionConfig, S3StorageService


@pytest.fixture
def s3_service() -> S3StorageService:
    config = S3ConnectionConfig(
        endpoint_url="http://seaweedfs-s3:8333",
        public_endpoint_url="http://localhost:8333",
        access_key="test_access_key",
        secret_key="test_secret_key",
        default_bucket="media",
        default_ttl_seconds=3600,
    )
    return S3StorageService(config=config)


@pytest.mark.asyncio
async def test_upload_bytes_success(s3_service: S3StorageService):
    mock_s3_client = AsyncMock()
    mock_s3_client.put_object = AsyncMock()

    mock_cm = MagicMock()
    mock_cm.__aenter__ = AsyncMock(return_value=mock_s3_client)
    mock_cm.__aexit__ = AsyncMock(return_value=None)

    with patch.object(s3_service, "_get_internal_client", return_value=mock_cm) as mock_get_internal:
        key = await s3_service.upload_bytes(
            bucket="media",
            key="test/sample.webp",
            data=b"fake-image-data",
            content_type="image/webp",
        )

        mock_get_internal.assert_called_once()
        mock_s3_client.put_object.assert_awaited_once_with(
            Bucket="media",
            Key="test/sample.webp",
            Body=b"fake-image-data",
            ContentType="image/webp",
        )
        assert key == "test/sample.webp"


@pytest.mark.asyncio
async def test_generate_presigned_url_uses_public_endpoint(s3_service: S3StorageService):
    mock_s3_client = AsyncMock()
    mock_s3_client.generate_presigned_url = AsyncMock(
        return_value="http://localhost:8333/media/test/sample.webp?X-Amz-Signature=xyz"
    )

    mock_cm = MagicMock()
    mock_cm.__aenter__ = AsyncMock(return_value=mock_s3_client)
    mock_cm.__aexit__ = AsyncMock(return_value=None)

    with patch.object(s3_service, "_get_public_client", return_value=mock_cm) as mock_get_public:
        url = await s3_service.generate_presigned_url(
            bucket="media",
            key="test/sample.webp",
            expires_in=7200,
        )

        # Ensure public client was used
        mock_get_public.assert_called_once()
        mock_s3_client.generate_presigned_url.assert_awaited_once_with(
            ClientMethod="get_object",
            Params={"Bucket": "media", "Key": "test/sample.webp"},
            ExpiresIn=7200,
        )
        assert "http://localhost:8333" in url


@pytest.mark.asyncio
async def test_delete_file_success(s3_service: S3StorageService):
    mock_s3_client = AsyncMock()
    mock_s3_client.delete_object = AsyncMock()

    mock_cm = MagicMock()
    mock_cm.__aenter__ = AsyncMock(return_value=mock_s3_client)
    mock_cm.__aexit__ = AsyncMock(return_value=None)

    with patch.object(s3_service, "_get_internal_client", return_value=mock_cm):
        await s3_service.delete_file(bucket="media", key="test/sample.webp")
        mock_s3_client.delete_object.assert_awaited_once_with(
            Bucket="media",
            Key="test/sample.webp",
        )


@pytest.mark.asyncio
async def test_get_bytes_success(s3_service: S3StorageService):
    mock_stream = AsyncMock()
    mock_stream.read = AsyncMock(return_value=b"retrieved-data")

    mock_body_cm = MagicMock()
    mock_body_cm.__aenter__ = AsyncMock(return_value=mock_stream)
    mock_body_cm.__aexit__ = AsyncMock(return_value=None)

    mock_s3_client = AsyncMock()
    mock_s3_client.get_object = AsyncMock(return_value={"Body": mock_body_cm})

    mock_cm = MagicMock()
    mock_cm.__aenter__ = AsyncMock(return_value=mock_s3_client)
    mock_cm.__aexit__ = AsyncMock(return_value=None)

    with patch.object(s3_service, "_get_internal_client", return_value=mock_cm):
        data = await s3_service.get_bytes(bucket="media", key="test/sample.webp")
        assert data == b"retrieved-data"


@pytest.mark.asyncio
async def test_get_bytes_not_found_raises_exception(s3_service: S3StorageService):
    mock_s3_client = AsyncMock()
    error_response = {"Error": {"Code": "NoSuchKey", "Message": "The specified key does not exist."}}
    mock_s3_client.get_object = AsyncMock(
        side_effect=ClientError(cast(Any, error_response), "GetObject")
    )

    mock_cm = MagicMock()
    mock_cm.__aenter__ = AsyncMock(return_value=mock_s3_client)
    mock_cm.__aexit__ = AsyncMock(return_value=None)

    with patch.object(s3_service, "_get_internal_client", return_value=mock_cm):
        with pytest.raises(S3ObjectNotFound):
            await s3_service.get_bytes(bucket="media", key="nonexistent.webp")


@pytest.mark.asyncio
async def test_object_exists_true_and_false(s3_service: S3StorageService):
    mock_s3_client = AsyncMock()
    mock_s3_client.head_object = AsyncMock()

    mock_cm = MagicMock()
    mock_cm.__aenter__ = AsyncMock(return_value=mock_s3_client)
    mock_cm.__aexit__ = AsyncMock(return_value=None)

    with patch.object(s3_service, "_get_internal_client", return_value=mock_cm):
        assert await s3_service.object_exists(bucket="media", key="existing.webp") is True

    # Test 404
    error_response = {"Error": {"Code": "404", "Message": "Not Found"}}
    mock_s3_client.head_object = AsyncMock(
        side_effect=ClientError(cast(Any, error_response), "HeadObject")
    )

    with patch.object(s3_service, "_get_internal_client", return_value=mock_cm):
        assert await s3_service.object_exists(bucket="media", key="missing.webp") is False
