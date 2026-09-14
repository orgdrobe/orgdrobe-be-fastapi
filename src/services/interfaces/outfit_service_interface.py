from abc import ABC, abstractmethod

from schemas.outfit import NewOutfit, UpdateOutfit, OutfitOut
from models import User


class OutfitServiceInterface(ABC):
    @abstractmethod
    async def create(self, user_id: int, new_outfit: NewOutfit) -> OutfitOut: ...

    @abstractmethod
    async def get_by_id(self, user_id: int, id: int) -> OutfitOut: ...

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[OutfitOut]: ...

    @abstractmethod
    async def update(self, user_id: int, id: int, update_data: UpdateOutfit) -> OutfitOut: ...

    @abstractmethod
    async def delete(self, user_id: int, id: int) -> bool: ...

