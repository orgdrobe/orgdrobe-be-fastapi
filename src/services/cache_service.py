from dataclasses import dataclass
from typing import Any

from cashews import cache

from services.interfaces import CacheServiceInterface
# ATTENTION: In‑memory cache does not work in multi‑worker applications (use Redis).


@dataclass
class CacheConfig:
    """Configuration parameters for cache backend and operations."""

    backend_url: str = "mem://"
    default_prefix: str = "app"
    default_ttl: int = 300


class CacheService(CacheServiceInterface):
    def __init__(self, config: CacheConfig | None = None) -> None:
        self.config = config or CacheConfig()

        if not cache.is_setup():
            cache.setup(self.config.backend_url)

        self._prefix = self.config.default_prefix
        self._default_ttl = self.config.default_ttl

    def _build_key(self, key: str) -> str:
        """Format cache key prefixed with current namespace."""
        return f"{self._prefix}:{key}"
    
    @property
    def prefix(self) -> str:
        """Get the current namespace prefix for cached keys."""
        return self._prefix

    @prefix.setter
    def prefix(self, value) -> None:
        """Set the namespace prefix for cached keys."""
        if not isinstance(value, str):
            raise ValueError("Prefix must be a string")
        self._prefix = value

    async def get(self, key: str) -> Any | None:
        """Retrieve cached value by key, or None if missing/expired."""
        return await cache.get(self._build_key(key))
    
    async def set(self, key: str, value: Any, ttl: int | str | None = None) -> bool:
        """Store a value under the specified key with an optional time-to-live (TTL)."""
        ttl = ttl or self._default_ttl
        return await cache.set(self._build_key(key), value, expire=ttl)

    async def delete(self, key: str) -> bool:
        """Delete an entry from cache by key."""
        return await cache.delete(self._build_key(key))

    async def exists(self, key: str) -> bool:
        """Check if an unexpired key exists in cache."""
        return await cache.exists(self._build_key(key))

    async def clear(self):
        """Clear all keys in the current cache backend."""
        await cache.clear()

    async def increment(self, key: str, ttl: int | str | None = None) -> int:
        """Atomically increment the integer value of a key with optional TTL."""
        full_key = self._build_key(key)
        new_value = await cache.incr(full_key)
        
        if new_value == 1 and ttl:
            await cache.expire(full_key, timeout=ttl)
            
        return new_value