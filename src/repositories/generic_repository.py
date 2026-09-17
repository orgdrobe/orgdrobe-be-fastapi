from typing import Any, Generic, Type, TypeVar, Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import GenericRepositoryInterface

class ModelWithId(Protocol):
    id: Any

T = TypeVar("T", bound=ModelWithId)

class GenericRepository(GenericRepositoryInterface[T], Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]) -> None:
        self._session = session
        self._model = model

    async def add(self, entity: T) -> T: 
        self._session.add(entity)
        await self._session.flush()
        return entity
    
    async def get_by_id(self, id: int) -> T | None:
        stmt = select(self._model).where(self._model.id == id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[T]: 
        stmt = select(self._model).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
    
    async def update(self, entity: T, update_data: dict[str, Any]) -> T | None:
        for key, value in update_data.items():
            setattr(entity, key, value)
            
        self._session.add(entity) 
        await self._session.flush()
        return entity
    
    async def delete(self, id: int) -> bool:
        entity = await self.get_by_id(id)
        if not entity:
            return False
            
        await self._session.delete(entity)
        await self._session.flush()
        return True