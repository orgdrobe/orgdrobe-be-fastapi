from typing import cast
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone
import pytest
from fastapi import UploadFile

from core.exceptions.garment_exceptions import GarmentNotFound, GarmentImageNotFound
from models import Garment, GarmentImage
from models.user_avatar import UserAvatar
from schemas.media import UploadedMediaOut
from services.garment_service import GarmentService
from services.user_service import UserService


@pytest.fixture
def mock_uow() -> MagicMock:
    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=None)
    uow.commit = AsyncMock()
    return uow


@pytest.fixture
def mock_media_service() -> AsyncMock:
    media = AsyncMock()
    media.upload_media.return_value = UploadedMediaOut(
        file_key="private/garments/1/test-uuid.webp",
        url="http://storage.local/media/test.webp",
        width=1000,
        height=1000,
        size_bytes=50000,
    )
    media.delete_media.return_value = None
    media.get_presigned_url.return_value = "http://storage.local/media/test.webp"
    return media


@pytest.mark.asyncio
async def test_garment_add_image_success(mock_uow: MagicMock, mock_media_service: AsyncMock):
    garment = Garment(id=1, user_id=10, name="Shirt")
    garment_repo = AsyncMock()
    garment_repo.get_by_id.return_value = garment

    image_repo = AsyncMock()
    image_repo.get_by_garment_id.return_value = []
    
    saved_image = GarmentImage(
        id=101,
        garment_id=1,
        image_key="private/garments/1/test-uuid.webp",
        is_primary=True,
        order=0,
        created_at=datetime.now(timezone.utc),
    )
    image_repo.add.return_value = saved_image

    def get_repo(interface):
        name = interface.__name__
        if "GarmentRepository" in name:
            return garment_repo
        if "GarmentImageRepository" in name:
            return image_repo
        return AsyncMock()

    mock_uow.get_repo_by_interface.side_effect = get_repo

    service = GarmentService(uow=mock_uow, media_service=mock_media_service)
    fake_file = cast(UploadFile, MagicMock(spec=UploadFile))

    result = await service.add_image(
        user_id=10,
        garment_id=1,
        file=fake_file,
        is_primary=False,
        order=0,
    )

    assert result.id == 101
    assert result.garment_id == 1
    assert result.url == "http://storage.local/media/test.webp"
    mock_media_service.upload_media.assert_awaited_once_with(
        file=fake_file,
        entity_type="garments",
        entity_id=1,
        user_id=10,
    )
    mock_uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_garment_delete_image_success(mock_uow: MagicMock, mock_media_service: AsyncMock):
    garment = Garment(id=1, user_id=10, name="Shirt")
    garment_repo = AsyncMock()
    garment_repo.get_by_id.return_value = garment

    image_repo = AsyncMock()
    image = GarmentImage(
        id=101,
        garment_id=1,
        image_key="private/garments/1/test-uuid.webp",
        is_primary=True,
        order=0,
    )
    image_repo.get_by_id.return_value = image
    image_repo.delete.return_value = True

    def get_repo(interface):
        name = interface.__name__
        if "GarmentRepository" in name:
            return garment_repo
        if "GarmentImageRepository" in name:
            return image_repo
        return AsyncMock()

    mock_uow.get_repo_by_interface.side_effect = get_repo

    service = GarmentService(uow=mock_uow, media_service=mock_media_service)

    success = await service.delete_image(user_id=10, garment_id=1, image_id=101)

    assert success is True
    mock_media_service.delete_media.assert_awaited_once_with(
        user_id=10, file_key="private/garments/1/test-uuid.webp"
    )
    image_repo.delete.assert_awaited_once_with(101)
    mock_uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_user_upload_avatar_success(mock_uow: MagicMock, mock_media_service: AsyncMock):
    avatar_repo = AsyncMock()
    avatar_repo.get_by_user_id.return_value = None

    saved_avatar = UserAvatar(
        id=5,
        user_id=42,
        image_key="private/users/42/test-avatar.webp",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    avatar_repo.add.return_value = saved_avatar

    mock_media_service.upload_media.return_value = UploadedMediaOut(
        file_key="private/users/42/test-avatar.webp",
        url="http://storage.local/media/avatar.webp",
        width=500,
        height=500,
        size_bytes=20000,
    )

    mock_uow.get_repo_by_interface.return_value = avatar_repo

    user_service = UserService(uow=mock_uow, media_service=mock_media_service)
    mock_file = MagicMock()
    mock_file.filename = "avatar.jpg"
    fake_file = cast(UploadFile, mock_file)

    result = await user_service.upload_avatar(user_id=42, file=fake_file)

    assert result.url == "http://storage.local/media/avatar.webp"
    mock_media_service.upload_media.assert_awaited_once_with(
        file=fake_file,
        entity_type="users",
        entity_id=42,
        user_id=42,
    )
    mock_uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_garment_add_images_batch_success(mock_uow: MagicMock, mock_media_service: AsyncMock):
    garment = Garment(id=1, user_id=10, name="Shirt")
    garment_repo = AsyncMock()
    garment_repo.get_by_id.return_value = garment

    image_repo = AsyncMock()
    image_repo.get_by_garment_id.return_value = []

    def make_saved_image(entity):
        entity.id = 100 + entity.order
        entity.created_at = datetime.now(timezone.utc)
        return entity

    image_repo.add.side_effect = make_saved_image

    def get_repo(interface):
        name = interface.__name__
        if "GarmentRepository" in name:
            return garment_repo
        if "GarmentImageRepository" in name:
            return image_repo
        return AsyncMock()

    mock_uow.get_repo_by_interface.side_effect = get_repo

    service = GarmentService(uow=mock_uow, media_service=mock_media_service)
    files = cast(
        list[UploadFile],
        [MagicMock(spec=UploadFile), MagicMock(spec=UploadFile)],
    )

    results = await service.add_images_batch(user_id=10, garment_id=1, files=files)

    assert len(results) == 2
    assert results[0].is_primary is True
    assert results[0].order == 0
    assert results[1].is_primary is False
    assert results[1].order == 1
    assert mock_media_service.upload_media.await_count == 2
    mock_uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_garment_delete_images_batch_success(mock_uow: MagicMock, mock_media_service: AsyncMock):
    garment = Garment(id=1, user_id=10, name="Shirt")
    garment_repo = AsyncMock()
    garment_repo.get_by_id.return_value = garment

    image1 = GarmentImage(id=101, garment_id=1, image_key="private/garments/1/k1.webp")
    image2 = GarmentImage(id=102, garment_id=1, image_key="private/garments/1/k2.webp")

    image_repo = AsyncMock()
    image_repo.get_by_id.side_effect = lambda img_id: image1 if img_id == 101 else image2 if img_id == 102 else None
    image_repo.delete.return_value = True

    def get_repo(interface):
        name = interface.__name__
        if "GarmentRepository" in name:
            return garment_repo
        if "GarmentImageRepository" in name:
            return image_repo
        return AsyncMock()

    mock_uow.get_repo_by_interface.side_effect = get_repo

    service = GarmentService(uow=mock_uow, media_service=mock_media_service)

    success = await service.delete_images_batch(user_id=10, garment_id=1, image_ids=[101, 102])

    assert success is True
    assert mock_media_service.delete_media.await_count == 2
    assert image_repo.delete.await_count == 2
    mock_uow.commit.assert_awaited_once()

