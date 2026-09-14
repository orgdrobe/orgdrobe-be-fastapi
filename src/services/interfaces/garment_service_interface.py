from abc import ABC, abstractmethod

from schemas.garment import UpdateGarment, NewGarment, GarmentOut
from models import User

class GarmentServiceInterface(ABC):
    @abstractmethod
    async def create(self, user_id: int, new_garment: NewGarment) -> GarmentOut: ...
    
    @abstractmethod
    async def get_by_id(self, user_id: int, id: int) -> GarmentOut: ...
    
    @abstractmethod
    async def get_all_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[GarmentOut]: ...
    
    @abstractmethod
    async def update(self, user_id: int, id: int, update_data: UpdateGarment) -> GarmentOut: ...
    
    @abstractmethod
    async def delete(self, user_id: int, id: int) -> bool: ...

