from abc import ABC, abstractmethod

from schemas.season import (
    NewSeason,
    SeasonOut,
    UpdateSeason,
)


class SeasonServiceInterface(ABC):
    """Interface for managing clothing seasonality categories (e.g. Summer, Winter, All-Season)."""

    @abstractmethod
    async def create(self, new_season: NewSeason) -> SeasonOut:
        """Create a new season category."""
        ...

    @abstractmethod
    async def get_by_id(self, id: int) -> SeasonOut:
        """Retrieve a season category by its unique ID."""
        ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[SeasonOut]:
        """Fetch a paginated list of all season categories."""
        ...

    @abstractmethod
    async def update(self, id: int, update_data: UpdateSeason) -> SeasonOut:
        """Update an existing season category."""
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Delete a season category by its unique ID."""
        ...
