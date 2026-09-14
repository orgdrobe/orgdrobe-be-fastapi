from abc import ABC, abstractmethod

from schemas.season import (
    NewSeason, 
    SeasonOut, 
    UpdateSeason
)


class SeasonServiceInterface(ABC):
    @abstractmethod
    async def create(self, new_season: NewSeason) -> SeasonOut: ...
    
    @abstractmethod
    async def get_by_id(self, id: int) -> SeasonOut: ...
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[SeasonOut]: ...
    
    @abstractmethod
    async def update(self, id: int, update_data: UpdateSeason) -> SeasonOut: ...
    
    @abstractmethod
    async def delete(self, id: int) -> bool: ...

