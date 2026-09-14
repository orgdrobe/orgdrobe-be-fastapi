from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import GarmentRepositoryInterface
from models import Garment, GarmentColor


class GarmentRepository(GarmentRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, garment: Garment) -> Garment: 
        self._session.add(garment)
        await self._session.flush()
        return garment

    async def get_by_id(self, id: int) -> Garment | None:
        stmt = (
            select(Garment)
            .where(Garment.id == id)
            .options(*self._eager_options())
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Garment | None:
        stmt = (
            select(Garment)
            .where(Garment.name == name)
            .options(*self._eager_options())
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_ids_and_user_id(self, ids: Sequence[int], user_id: int) -> list[Garment]:
        if not ids:
            return []
        stmt = (
            select(Garment)
            .where(Garment.id.in_(ids), Garment.user_id == user_id)
            .options(*self._eager_options())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_all_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Garment]: 
        stmt = (
            select(Garment)
            .where(Garment.user_id == user_id)
            .options(*self._eager_options())
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
        
    async def update(self, garment: Garment, update_data: dict[str, Any]) -> Garment | None:
        for key, value in update_data.items():
            setattr(garment, key, value)

        self._session.add(garment)
        await self._session.flush()
        return garment
        
    async def delete(self, id: int) -> bool:
        stmt = select(Garment).where(Garment.id == id)
        result = await self._session.execute(stmt)
        garment = result.scalar_one_or_none()
        if not garment:
            return False
                    
        await self._session.delete(garment)
        await self._session.flush()
        return True

    @staticmethod
    def _eager_options():
        return [
            selectinload(Garment.gender),
            selectinload(Garment.category_master),
            selectinload(Garment.category_sub),
            selectinload(Garment.garment_type),
            selectinload(Garment.season),
            selectinload(Garment.usage),
            selectinload(Garment.colors).joinedload(GarmentColor.color),
        ]