from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import RefreshTokenRepositoryInterface
from models import RefreshToken, User

class RefreshTokenRepository(RefreshTokenRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_jti(self, jti: UUID) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.jti == jti)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_jti_with_user_and_roles(self, jti: UUID) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.jti == jti).options(
            joinedload(RefreshToken.user).selectinload(User.roles)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, refresh_token: RefreshToken) -> RefreshToken:
        self._session.add(refresh_token)
        await self._session.flush()
        return refresh_token