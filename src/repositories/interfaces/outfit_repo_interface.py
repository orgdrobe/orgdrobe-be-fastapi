from typing import Any, Sequence
from abc import ABC, abstractmethod

from models import Outfit


class OutfitRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Outfit | None: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> Outfit | None: ...

    @abstractmethod
    async def add(self, outfit: Outfit) -> Outfit: ...

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> Sequence[Outfit]: ...

    @abstractmethod
    async def update(self, outfit: Outfit, update_data: dict[str, Any]) -> Outfit | None: ...

    @abstractmethod
    async def delete(self, id: int) -> bool: ...

