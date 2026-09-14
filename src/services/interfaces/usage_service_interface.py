from abc import ABC, abstractmethod

from schemas.usage import (
    NewUsage, 
    UsageOut, 
    UpdateUsage
)


class UsageServiceInterface(ABC):
    @abstractmethod
    async def create(self, new_usage: NewUsage) -> UsageOut: ...
    
    @abstractmethod
    async def get_by_id(self, id: int) -> UsageOut: ...
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[UsageOut]: ...
    
    @abstractmethod
    async def update(self, id: int, update_data: UpdateUsage) -> UsageOut: ...
    
    @abstractmethod
    async def delete(self, id: int) -> bool: ...

