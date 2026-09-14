from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import OutfitRepositoryInterface
from models import Outfit, OutfitColor, Garment, GarmentColor


class OutfitRepository(OutfitRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, outfit: Outfit) -> Outfit:
        self._session.add(outfit)
        await self._session.flush()
        return outfit

    async def get_by_id(self, id: int) -> Outfit | None:
        stmt = (
            select(Outfit)
            .where(Outfit.id == id)
            .options(*self._eager_options())
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Outfit | None:
        stmt = (
            select(Outfit)
            .where(Outfit.name == name)
            .options(*self._eager_options())
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Outfit]:
        stmt = (
            select(Outfit)
            .where(Outfit.user_id == user_id)
            .options(*self._eager_options())
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, outfit: Outfit, update_data: dict[str, Any]) -> Outfit | None:
        for key, value in update_data.items():
            setattr(outfit, key, value)

        self._session.add(outfit)
        await self._session.flush()
        return outfit

    async def delete(self, id: int) -> bool:
        stmt = select(Outfit).where(Outfit.id == id)
        result = await self._session.execute(stmt)
        outfit = result.scalar_one_or_none()
        if not outfit:
            return False

        await self._session.delete(outfit)
        await self._session.flush()
        return True

    @staticmethod
    def _eager_options():
        return [
            selectinload(Outfit.garments).options(
                selectinload(Garment.gender),
                selectinload(Garment.category_master),
                selectinload(Garment.category_sub),
                selectinload(Garment.garment_type),
                selectinload(Garment.season),
                selectinload(Garment.usage),
                selectinload(Garment.colors).joinedload(GarmentColor.color),
            ),
            selectinload(Outfit.colors).joinedload(OutfitColor.color),
        ]