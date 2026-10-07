from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import GarmentImageRepositoryInterface
from repositories.generic_repository import GenericRepository
from models import GarmentImage


class GarmentImageRepository(GenericRepository[GarmentImage], GarmentImageRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, GarmentImage)

    async def get_by_garment_id(self, garment_id: int) -> list[GarmentImage]:
        stmt = (
            select(GarmentImage)
            .where(GarmentImage.garment_id == garment_id)
            .order_by(GarmentImage.order)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

