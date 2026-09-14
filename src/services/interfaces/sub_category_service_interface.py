from abc import ABC, abstractmethod

from schemas.sub_category import (
    NewSubCategory, 
    SubCategoryOut, 
    UpdateSubCategory
)

class SubCategoryServiceInterface(ABC):
    @abstractmethod
    async def create(self, new_category_master: NewSubCategory) -> SubCategoryOut: ...
    
    @abstractmethod
    async def get_by_id(self, id: int) -> SubCategoryOut: ...
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[SubCategoryOut]: ...
    
    @abstractmethod
    async def update(self, id: int, update_data: UpdateSubCategory) -> SubCategoryOut: ...
    
    @abstractmethod
    async def delete(self, id: int) -> bool: ...