from abc import ABC, abstractmethod

from fastapi import UploadFile

from schemas.user import UserAvatarOut


class UserServiceInterface(ABC):
    """Interface for user profile management including avatar storage."""

    @abstractmethod
    async def upload_avatar(
        self, user_id: int, file: UploadFile
    ) -> UserAvatarOut:
        """Upload, validate, and store a new user avatar, replacing any existing avatar."""
        ...

    @abstractmethod
    async def get_avatar(self, user_id: int) -> UserAvatarOut | None:
        """Retrieve the user's avatar with its fresh presigned URL."""
        ...

    @abstractmethod
    async def delete_avatar(self, user_id: int) -> bool:
        """Delete user avatar from storage, cache, and database."""
        ...

