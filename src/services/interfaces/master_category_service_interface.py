from abc import ABC, abstractmethod

from schemas.master_category import (
    MasterCategoryOut,
    NewMasterCategory,
    UpdateMasterCategory,
)


class MasterCategoryServiceInterface(ABC):
    """Interface for managing top-level garment master categories (e.g. Apparel, Footwear)."""

    @abstractmethod
    async def create(self, new_category_master: NewMasterCategory) -> MasterCategoryOut:
        """Create a new master category."""
        ...

    @abstractmethod
    async def get_by_id(self, id: int) -> MasterCategoryOut:
        """Retrieve a master category by its unique ID."""
        ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[MasterCategoryOut]:
        """Fetch a paginated list of all master categories."""
        ...

    @abstractmethod
    async def update(
        self, id: int, update_data: UpdateMasterCategory
    ) -> MasterCategoryOut:
        """Update an existing master category's attributes."""
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Delete a master category by its unique ID."""
        ...