from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import UserRoleRepositoryInterface
from models import UserRole 

class UserRoleRepository(UserRoleRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, user_role: UserRole) -> UserRole:
        self._session.add(user_role)
        await self._session.flush()
        await self._session.refresh(user_role)
        return user_role