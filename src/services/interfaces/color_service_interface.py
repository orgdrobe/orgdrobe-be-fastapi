from abc import ABC, abstractmethod

from schemas.color import (
    ColorOut,
    NewColor,
    UpdateColor,
)


class ColorServiceInterface(ABC):
    """Interface for managing standard garment colors and palette entities."""

    @abstractmethod
    async def create(self, new_color: NewColor) -> ColorOut:
        """Create a new color entity."""
        ...

    @abstractmethod
    async def get_by_id(self, id: int) -> ColorOut:
        """Retrieve a color by its unique ID."""
        ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ColorOut]:
        """Fetch a paginated list of all colors."""
        ...

    @abstractmethod
    async def update(self, id: int, update_data: UpdateColor) -> ColorOut:
        """Update an existing color's details."""
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Delete a color by its unique ID."""
        ...
