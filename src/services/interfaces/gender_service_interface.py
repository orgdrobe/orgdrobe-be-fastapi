from abc import ABC, abstractmethod

from schemas.gender import (
    GenderOut,
    NewGender,
    UpdateGender,
)


class GenderServiceInterface(ABC):
    """Interface for managing target gender classifications (e.g. Men, Women, Unisex)."""

    @abstractmethod
    async def create(self, new_gender: NewGender) -> GenderOut:
        """Create a new gender classification."""
        ...

    @abstractmethod
    async def get_by_id(self, id: int) -> GenderOut:
        """Retrieve a gender classification by its unique ID."""
        ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[GenderOut]:
        """Fetch a paginated list of all gender classifications."""
        ...

    @abstractmethod
    async def update(self, id: int, update_data: UpdateGender) -> GenderOut:
        """Update an existing gender classification."""
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Delete a gender classification by its unique ID."""
        ...
