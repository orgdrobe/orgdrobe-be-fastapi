from abc import ABC, abstractmethod
from typing import Callable, Self, Type, TypeVar

R = TypeVar("R")


class UnitOfWorkInterface(ABC):
    """Interface for atomic transaction lifecycle and scoped repository resolution."""

    @abstractmethod
    async def __aenter__(self) -> Self:
        """Enter the asynchronous transaction context."""
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the asynchronous transaction context, rolling back on unhandled error."""
        ...

    @abstractmethod
    async def commit(self) -> None:
        """Commit all pending database operations in the active transaction."""
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """Roll back all pending database operations in the active transaction."""
        ...

    @abstractmethod
    def get_repo(self, repo_type: Type[R]) -> R:
        """Retrieve a repository instance by concrete class bound to the current session."""
        ...

    @abstractmethod
    def get_repo_by_interface(self, interface: Callable[..., R]) -> R:
        """Retrieve a repository instance matching the given interface contract."""
        ...