from abc import ABC, abstractmethod
from typing import Any


class CacheServiceInterface(ABC):
    """Interface for asynchronous key-value caching and rate-limiting storage."""

    @property
    @abstractmethod
    def prefix(self) -> str:
        """Get the current namespace prefix for cached keys."""
        ...

    @prefix.setter
    @abstractmethod
    def prefix(self, value: str) -> None:
        """Set the namespace prefix for cached keys."""
        ...

    @abstractmethod
    async def get(self, key: str) -> Any | None:
        """Retrieve cached value by key, or None if missing/expired."""
        ...

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int | str | None = None) -> bool:
        """Store a value under the specified key with an optional time-to-live (TTL)."""
        ...

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete an entry from cache by key."""
        ...

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if an unexpired key exists in cache."""
        ...

    @abstractmethod
    async def clear(self) -> None:
        """Clear all keys in the current namespace or database."""
        ...

    @abstractmethod
    async def increment(self, key: str, ttl: int | str | None = None) -> int:
        """Atomically increment the integer value of a key with optional TTL."""
        ...