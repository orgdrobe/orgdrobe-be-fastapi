from abc import ABC, abstractmethod

from schemas.sub_category import (
    NewSubCategory,
    SubCategoryOut,
    UpdateSubCategory,
)


class SubCategoryServiceInterface(ABC):
    """Interface for managing garment sub-categories (e.g. Topwear, Bottomwear)."""

    @abstractmethod
    async def create(self, new_category_master: NewSubCategory) -> SubCategoryOut:
        """Create a new sub-category associated with a master category."""
        ...

    @abstractmethod
    async def get_by_id(self, id: int) -> SubCategoryOut:
        """Retrieve a sub-category by its unique ID."""
        ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[SubCategoryOut]:
        """Fetch a paginated list of all sub-categories."""
        ...

    @abstractmethod
    async def update(
        self, id: int, update_data: UpdateSubCategory
    ) -> SubCategoryOut:
        """Update an existing sub-category's attributes."""
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Delete a sub-category by its unique ID."""
        ...