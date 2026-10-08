from abc import ABC, abstractmethod

from fastapi import UploadFile

from schemas.outfit import (
    NewOutfit,
    OutfitImageOut,
    OutfitOut,
    UpdateOutfit,
)


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

    @abstractmethod
    async def add_image(
        self,
        user_id: int,
        outfit_id: int,
        file: UploadFile,
        is_primary: bool = False,
        order: int = 0,
    ) -> OutfitImageOut:
        """Upload, validate, and associate an image with an existing user outfit."""
        ...

    @abstractmethod
    async def delete_image(
        self, user_id: int, outfit_id: int, image_id: int
    ) -> bool:
        """Remove an outfit image from storage, cache, and database."""
        ...

    @abstractmethod
    async def add_images_batch(
        self,
        user_id: int,
        outfit_id: int,
        files: list[UploadFile],
    ) -> list[OutfitImageOut]:
        """Upload, validate, and associate multiple images with an outfit in batch."""
        ...

    @abstractmethod
    async def delete_images_batch(
        self,
        user_id: int,
        outfit_id: int,
        image_ids: list[int],
    ) -> bool:
        """Remove multiple outfit images from storage, cache, and database in batch."""
        ...


