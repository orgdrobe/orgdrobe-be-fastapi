from abc import ABC, abstractmethod

from schemas.outfit import NewOutfit, OutfitOut, UpdateOutfit


class OutfitServiceInterface(ABC):
    """Interface for managing user outfits composed of wardrobe garments."""

    @abstractmethod
    async def create(self, user_id: int, new_outfit: NewOutfit) -> OutfitOut:
        """Create a new outfit composed of garments for the specified user."""
        ...

    @abstractmethod
    async def get_by_id(self, user_id: int, id: int) -> OutfitOut:
        """Retrieve a specific outfit by its ID for the authenticated user."""
        ...

    @abstractmethod
    async def get_all_by_user_id(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[OutfitOut]:
        """Fetch a paginated list of outfits belonging to the specified user."""
        ...

    @abstractmethod
    async def update(
        self, user_id: int, id: int, update_data: UpdateOutfit
    ) -> OutfitOut:
        """Update an existing outfit's details or constituent garments."""
        ...

    @abstractmethod
    async def delete(self, user_id: int, id: int) -> bool:
        """Delete an outfit item owned by the user."""
        ...
