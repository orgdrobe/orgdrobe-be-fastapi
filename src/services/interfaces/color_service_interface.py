from abc import ABC, abstractmethod

from schemas.color import (
    NewColor, 
    ColorOut, 
    UpdateColor
)

class ColorServiceInterface(ABC):
    @abstractmethod
    async def create(self, new_color: NewColor) -> ColorOut: ...
    
    @abstractmethod
    async def get_by_id(self, id: int) -> ColorOut: ...
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ColorOut]: ...
    
    @abstractmethod
    async def update(self, id: int, update_data: UpdateColor) -> ColorOut: ...
    
    @abstractmethod
    async def delete(self, id: int) -> bool: ...

