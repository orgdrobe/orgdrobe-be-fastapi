from abc import ABC, abstractmethod

from schemas.garment import GarmentOut, NewGarment, UpdateGarment


class GarmentServiceInterface(ABC):
    """Interface for managing wardrobe garment items and clothing assets."""

    @abstractmethod
    async def create(self, user_id: int, new_garment: NewGarment) -> GarmentOut:
        """Create a new garment item for the specified user."""
        ...

    @abstractmethod
    async def get_by_id(self, user_id: int, id: int) -> GarmentOut:
        """Retrieve a specific garment by its ID for the authenticated user."""
        ...

    @abstractmethod
    async def get_all_by_user_id(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[GarmentOut]:
        """Fetch a paginated list of garments belonging to the specified user."""
        ...

    @abstractmethod
    async def update(
        self, user_id: int, id: int, update_data: UpdateGarment
    ) -> GarmentOut:
        """Update an existing garment item's details."""
        ...

    @abstractmethod
    async def delete(self, user_id: int, id: int) -> bool:
        """Delete a garment item owned by the user."""
        ...
