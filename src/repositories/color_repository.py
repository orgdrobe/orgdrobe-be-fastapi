from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import ColorRepositoryInterface
from repositories.generic_repository import GenericRepository
from models import Color


class ColorRepository(GenericRepository[Color], ColorRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Color)

    async def get_by_rgb(self, red: int, green: int, blue: int) -> Color | None:
        stmt = select(Color).where(
            Color.red == red,
            Color.green == green,
            Color.blue == blue
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

