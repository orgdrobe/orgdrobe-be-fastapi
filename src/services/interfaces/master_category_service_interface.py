from abc import ABC, abstractmethod

from schemas.master_category import (
    NewMasterCategory, 
    MasterCategoryOut, 
    UpdateMasterCategory
)

class MasterCategoryServiceInterface(ABC):
    @abstractmethod
    async def create(self, new_category_master: NewMasterCategory) -> MasterCategoryOut: ...
    
    @abstractmethod
    async def get_by_id(self, id: int) -> MasterCategoryOut: ...
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[MasterCategoryOut]: ...
    
    @abstractmethod
    async def update(self, id: int, update_data: UpdateMasterCategory) -> MasterCategoryOut: ...
    
    @abstractmethod
    async def delete(self, id: int) -> bool: ...