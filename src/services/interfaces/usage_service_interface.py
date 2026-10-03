from abc import ABC, abstractmethod

from schemas.usage import (
    NewUsage,
    UpdateUsage,
    UsageOut,
)


class UsageServiceInterface(ABC):
    """Interface for managing garment occasions/usage categories (e.g. Casual, Formal, Sport)."""

    @abstractmethod
    async def create(self, new_usage: NewUsage) -> UsageOut:
        """Create a new clothing usage or occasion category."""
        ...

    @abstractmethod
    async def get_by_id(self, id: int) -> UsageOut:
        """Retrieve a usage category by its unique ID."""
        ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[UsageOut]:
        """Fetch a paginated list of all usage categories."""
        ...

    @abstractmethod
    async def update(self, id: int, update_data: UpdateUsage) -> UsageOut:
        """Update an existing usage category."""
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Delete a usage category by its unique ID."""
        ...
