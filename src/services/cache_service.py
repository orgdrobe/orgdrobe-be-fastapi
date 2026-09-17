from typing import Any

from cashews import cache

from services.interfaces import CacheServiceInterface
# ATTENTION: In‑memory cache does not work in multi‑worker applications (use Redis).

class CacheService(CacheServiceInterface):
    def __init__(self, backend_url: str = "mem://", default_prefix: str = "app", default_ttl: int = 300) -> None:
        if not cache.is_setup():
            cache.setup(backend_url)

        self._prefix = default_prefix
        self._default_ttl = default_ttl

    def _build_key(self, key: str) -> str:
        return f"{self._prefix}:{key}"
    
    @property
    def prefix(self) -> str:
        return self._prefix

    @prefix.setter
    def prefix(self, value) -> None:
        if not isinstance(value, str):
            raise ValueError("Prefix must be a string")
        self._prefix = value

    async def get(self, key: str) -> Any | None:
        return await cache.get(self._build_key(key))
    
    async def set(self, key: str, value: Any, ttl: int | str | None = None) -> bool:
        ttl = ttl or self._default_ttl
        return await cache.set(self._build_key(key), value, expire=ttl)

    async def delete(self, key: str) -> bool:
        return await cache.delete(self._build_key(key))

    async def exists(self, key: str) -> bool:
        return await cache.exists(self._build_key(key))

    async def clear(self):
        await cache.clear()

    async def increment(self, key: str, ttl: int | str | None = None) -> int:
        full_key = self._build_key(key)
        new_value = await cache.incr(full_key)
        
        if new_value == 1 and ttl:
            await cache.expire(full_key, timeout=ttl)
            
        return new_value