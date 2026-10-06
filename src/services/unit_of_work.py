from typing import Callable, TypeVar, Type, Any, Self, cast
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from services.interfaces import UnitOfWorkInterface

R = TypeVar("R")

class SqlAlchemyUnitOfWork(UnitOfWorkInterface):
    
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

        self._repositories: dict[Any, Any] = {}
        self._factories: dict[Any, Callable[[AsyncSession], Any]] = {}

    def register_factory(self, repo_type: Type[R], factory: Callable[[AsyncSession], R]) -> None:
        """Register a repository factory function by concrete class type."""
        self._factories[repo_type] = factory

    def register_factory_by_interface(self, interface: Callable[..., R], factory: Callable[[AsyncSession], R]) -> None:
        """Register a repository factory function by interface type."""
        self._factories[interface] = factory

    async def __aenter__(self) -> Self:
        """Start the Unit of Work and initialize database session."""
        self._session = self._session_factory()
        return self
    
    async def __aexit__(self, exc_type: Type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        """Exit the Unit of Work, roll back on error, and close session."""
        if not self._session:
            return
    
        try:
            if exc_type:
                await self.rollback()
            else:
                # can be explicit commit if we need
                # await self.commit()
                pass
        finally:
            await self._session.close()
            self._session = None
            self._repositories = {}
        
    async def commit(self) -> None:
        """Commit pending database transaction."""
        if self._session:
            await self._session.commit()

    async def rollback(self) -> None:
        """Roll back active database transaction."""
        if self._session:
            await self._session.rollback()
     
    def get_repo(self, repo_type: Type[R]) -> R:
        """Retrieve or lazily instantiate repository by concrete type."""
        if self._session is None:
            raise RuntimeError("Unit of Work has not been started. Use async with uow:")
        
        if repo_type in self._repositories:
            return self._repositories[repo_type]
        
        if repo_type not in self._factories:
            raise KeyError(f"Factory for repository '{repo_type.__name__}' is not registered.")
        
        factory = self._factories[repo_type]
        new_repo = factory(self._session)
        if not isinstance(new_repo, repo_type):
            raise TypeError(
                f"Factory for '{repo_type.__name__}' returned an object of type "
                f"'{type(new_repo).__name__}', which is not an instance of '{repo_type.__name__}'."
            )
        self._repositories[repo_type] = new_repo

        return new_repo

    def get_repo_by_interface(self, interface: Callable[..., R]) -> R:
        """Retrieve or lazily instantiate repository bound to the interface."""
        if self._session is None:
            raise RuntimeError("Unit of Work has not been started. Use async with uow:")
        
        if interface in self._repositories:
            return cast(R, self._repositories[interface])
        
        if interface not in self._factories:
            name = getattr(interface, '__name__', str(interface))
            raise KeyError(f"Factory for interface '{name}' is not registered.")
        
        factory = self._factories[interface]
        new_repo = factory(self._session)
        if isinstance(interface, type):
            try:
                if not isinstance(new_repo, interface):
                    name = getattr(interface, '__name__', str(interface))
                    raise TypeError(
                        f"Factory for interface '{name}' returned an object of type "
                        f"'{type(new_repo).__name__}', which does not implement '{name}'."
                    )
            except TypeError:
                pass
        self._repositories[interface] = new_repo

        return cast(R, new_repo)

