from abc import ABC, abstractmethod
from fastapi import UploadFile

from schemas.garment import (
    GarmentImageOut,
    GarmentOut,
    NewGarment,
    UpdateGarment,
)


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

    @abstractmethod
    async def add_image(
        self,
        user_id: int,
        garment_id: int,
        file: UploadFile,
        is_primary: bool = False,
        order: int = 0,
    ) -> GarmentImageOut:
        """Upload, validate, and associate an image with an existing user garment."""
        ...

    @abstractmethod
    async def delete_image(
        self, user_id: int, garment_id: int, image_id: int
    ) -> bool:
        """Remove a garment image from storage, cache, and database."""
        ...

    @abstractmethod
    async def add_images_batch(
        self,
        user_id: int,
        garment_id: int,
        files: list[UploadFile],
    ) -> list[GarmentImageOut]:
        """Upload, validate, and associate multiple images with a garment in batch."""
        ...

    @abstractmethod
    async def delete_images_batch(
        self,
        user_id: int,
        garment_id: int,
        image_ids: list[int],
    ) -> bool:
        """Remove multiple garment images from storage, cache, and database in batch."""
        ...


