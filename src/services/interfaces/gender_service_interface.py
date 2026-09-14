from abc import ABC, abstractmethod

from schemas.gender import (
    NewGender, 
    GenderOut, 
    UpdateGender
)


class GenderServiceInterface(ABC):
    @abstractmethod
    async def create(self, new_gender: NewGender) -> GenderOut: ...
    
    @abstractmethod
    async def get_by_id(self, id: int) -> GenderOut: ...
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[GenderOut]: ...
    
    @abstractmethod
    async def update(self, id: int, update_data: UpdateGender) -> GenderOut: ...
    
    @abstractmethod
    async def delete(self, id: int) -> bool: ...

