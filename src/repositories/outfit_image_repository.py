from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import OutfitImageRepositoryInterface
from repositories.generic_repository import GenericRepository
from models import OutfitImage


class OutfitImageRepository(GenericRepository[OutfitImage], OutfitImageRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, OutfitImage)

    async def get_by_outfit_id(self, outfit_id: int) -> list[OutfitImage]:
        stmt = (
            select(OutfitImage)
            .where(OutfitImage.outfit_id == outfit_id)
            .order_by(OutfitImage.order)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

