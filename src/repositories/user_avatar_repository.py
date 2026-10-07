from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import UserAvatarRepositoryInterface
from repositories.generic_repository import GenericRepository
from models import UserAvatar


class UserAvatarRepository(GenericRepository[UserAvatar], UserAvatarRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserAvatar)

    async def get_by_user_id(self, user_id: int) -> UserAvatar | None:
        stmt = select(UserAvatar).where(UserAvatar.user_id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_by_user_id(self, user_id: int) -> bool:
        avatar = await self.get_by_user_id(user_id)
        if not avatar:
            return False
        await self._session.delete(avatar)
        await self._session.flush()
        return True

