from typing import Any, Sequence
from abc import ABC, abstractmethod

from models import Garment

class GarmentRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Garment | None: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> Garment | None: ...

    @abstractmethod
    async def get_by_ids_and_user_id(self, ids: Sequence[int], user_id: int) -> Sequence[Garment]: ...
    
    @abstractmethod 
    async def add(self, garment: Garment) -> Garment: ...

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> Sequence[Garment]: ...

    @abstractmethod
    async def update(self, garment: Garment, update_data: dict[str, Any]) -> Garment | None: ...

    @abstractmethod
    async def delete(self, id: int) -> bool: ...
