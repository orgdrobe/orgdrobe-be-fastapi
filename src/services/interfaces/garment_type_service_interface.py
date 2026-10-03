from abc import ABC, abstractmethod

from schemas.garment_type import (
    GarmentTypeOut,
    NewGarmentType,
    UpdateGarmentType,
)


class GarmentTypeServiceInterface(ABC):
    """Interface for managing specific garment types (e.g. T-Shirt, Jeans, Hoodie)."""

    @abstractmethod
    async def create(self, new_garment_type: NewGarmentType) -> GarmentTypeOut:
        """Create a new garment type associated with a sub-category."""
        ...

    @abstractmethod
    async def get_by_id(self, id: int) -> GarmentTypeOut:
        """Retrieve a garment type by its unique ID."""
        ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[GarmentTypeOut]:
        """Fetch a paginated list of all garment types."""
        ...

    @abstractmethod
    async def update(
        self, id: int, update_data: UpdateGarmentType
    ) -> GarmentTypeOut:
        """Update an existing garment type's attributes."""
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Delete a garment type by its unique ID."""
        ...
