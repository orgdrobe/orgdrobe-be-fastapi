from typing import Any
from abc import ABC, abstractmethod

class CacheServiceInterface(ABC):
    
    @property
    @abstractmethod
    def prefix(self) -> str: ...

    @prefix.setter
    @abstractmethod
    def prefix(self,value) -> None: ...

    @abstractmethod
    async def get(self, key: str) -> Any | None: ...
        
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int | str | None = None) -> bool: ...

    @abstractmethod  
    async def delete(self, key: str) -> bool: ...
      
    @abstractmethod
    async def exists(self, key: str) -> bool: ...
      
    @abstractmethod
    async def clear(self) -> None: ...

    @abstractmethod
    async def increment(self, key: str, ttl: int | str | None = None) -> int: ...
       