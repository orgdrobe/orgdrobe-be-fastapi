from typing import Any, Generic, Type, TypeVar, Sequence
from abc import ABC, abstractmethod

T = TypeVar("T")

class GenericRepositoryInterface(ABC, Generic[T]):
    @abstractmethod
    async def add(self, obj: T) -> T: ...

    @abstractmethod
    async def get_by_id(self, id: int) -> T | None: ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[T]: ...

    @abstractmethod
    async def update(self, obj: T, update_data: dict[str, Any]) -> T | None: ...

    @abstractmethod
    async def delete(self, id: int) -> bool: ...
