from fastapi import UploadFile
import structlog

from core.exceptions.image_exceptions import UserAvatarNotFound
from models.user_avatar import UserAvatar
from repositories.interfaces import UserAvatarRepositoryInterface
from schemas.user import UserAvatarOut
from services.interfaces.media_service_interface import MediaServiceInterface
from services.interfaces.unit_of_work_interface import UnitOfWorkInterface
from services.interfaces.user_service_interface import UserServiceInterface

logger = structlog.get_logger()


class UserService(UserServiceInterface):
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        media_service: MediaServiceInterface,
    ) -> None:
        self._uow = uow
        self._media_service = media_service

    async def upload_avatar(
        self, user_id: int, file: UploadFile
    ) -> UserAvatarOut:
        """Upload, validate, and store a new user avatar, deleting any old avatar."""
        logger.info("uploading_user_avatar", user_id=user_id, filename=getattr(file, "filename", None))

        async with self._uow as uow:
            avatar_repo = uow.get_repo_by_interface(
                UserAvatarRepositoryInterface
            )
            existing_avatar = await avatar_repo.get_by_user_id(user_id)

            if existing_avatar:
                logger.info(
                    "deleting_old_avatar",
                    user_id=user_id,
                    old_key=existing_avatar.image_key,
                )
                await self._media_service.delete_media(
                    user_id=user_id, file_key=existing_avatar.image_key
                )

            uploaded = await self._media_service.upload_media(
                file=file,
                entity_type="users",
                entity_id=user_id,
                user_id=user_id,
            )

            if existing_avatar:
                existing_avatar.image_key = uploaded.file_key
                await avatar_repo.update(
                    existing_avatar, {"image_key": uploaded.file_key}
                )
                avatar = existing_avatar
            else:
                avatar = UserAvatar(
                    user_id=user_id,
                    image_key=uploaded.file_key,
                )
                avatar = await avatar_repo.add(avatar)

            await uow.commit()

            return UserAvatarOut(url=uploaded.url)

    async def get_avatar(self, user_id: int) -> UserAvatarOut | None:
        """Retrieve the user's avatar with its fresh presigned URL."""
        async with self._uow as uow:
            avatar_repo = uow.get_repo_by_interface(
                UserAvatarRepositoryInterface
            )
            avatar = await avatar_repo.get_by_user_id(user_id)
            if not avatar:
                return None

            url = await self._media_service.get_presigned_url(
                user_id=user_id, file_key=avatar.image_key
            )
            return UserAvatarOut(url=url)

    async def delete_avatar(self, user_id: int) -> bool:
        """Delete user avatar from storage, cache, and database."""
        logger.info("deleting_user_avatar", user_id=user_id)
        async with self._uow as uow:
            avatar_repo = uow.get_repo_by_interface(
                UserAvatarRepositoryInterface
            )
            avatar = await avatar_repo.get_by_user_id(user_id)
            if not avatar:
                raise UserAvatarNotFound(user_id)

            await self._media_service.delete_media(
                user_id=user_id, file_key=avatar.image_key
            )
            await avatar_repo.delete(avatar.id)
            await uow.commit()
            return True

