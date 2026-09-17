from abc import ABC, abstractmethod
from typing import Type, TypeVar, Self, Callable

R = TypeVar("R")

class UnitOfWorkInterface(ABC):
    @abstractmethod
    async def __aenter__(self) -> Self: ...
    
    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...
    
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    def get_repo(self, repo_type: Type[R]) -> R: ...

    @abstractmethod
    def get_repo_by_interface(self, interface: Callable[..., R]) -> R: ...