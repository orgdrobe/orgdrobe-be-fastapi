from abc import abstractmethod
from .generic_repo_interface import GenericRepositoryInterface
from models import UserAvatar


class UserAvatarRepositoryInterface(GenericRepositoryInterface[UserAvatar]):
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> UserAvatar | None: ...

    @abstractmethod
    async def delete_by_user_id(self, user_id: int) -> bool: ...

