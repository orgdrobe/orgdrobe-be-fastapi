from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import UserIdentityRepositoryInterface
from models import UserIdentity, User

class UserIdentityRepository(UserIdentityRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_user_id(self, user_id: int) -> UserIdentity | None:
        stmt = select(UserIdentity).where(UserIdentity.user_id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_provider_id(self, user_provider_id: str) -> UserIdentity | None:
        stmt = select(UserIdentity).where(UserIdentity.provider_id == user_provider_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_provider_id_with_user_and_roles(self, user_provider_id: str) -> UserIdentity | None:
        stmt = select(UserIdentity).where(UserIdentity.provider_id == user_provider_id).options(
            joinedload(UserIdentity.user).selectinload(User.roles)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, user_identity: UserIdentity) -> UserIdentity:
        self._session.add(user_identity)
        await self._session.flush()
        await self._session.refresh(user_identity)
        return user_identity