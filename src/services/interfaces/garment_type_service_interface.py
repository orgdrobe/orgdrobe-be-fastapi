from abc import ABC, abstractmethod

from schemas.garment_type import (
    NewGarmentType, 
    GarmentTypeOut, 
    UpdateGarmentType
)


class GarmentTypeServiceInterface(ABC):
    @abstractmethod
    async def create(self, new_garment_type: NewGarmentType) -> GarmentTypeOut: ...
    
    @abstractmethod
    async def get_by_id(self, id: int) -> GarmentTypeOut: ...
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[GarmentTypeOut]: ...
    
    @abstractmethod
    async def update(self, id: int, update_data: UpdateGarmentType) -> GarmentTypeOut: ...
    
    @abstractmethod
    async def delete(self, id: int) -> bool: ...

