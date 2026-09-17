from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from repositories.interfaces import RoleRepositoryInterface
from models import Role 

class RoleRepository(RoleRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_name(self, role_name: str) -> Role | None:
        stmt = select(Role).where(Role.name == role_name)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()