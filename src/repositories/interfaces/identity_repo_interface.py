from abc import ABC, abstractmethod

from models import UserIdentity

class UserIdentityRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> UserIdentity | None: ...

    @abstractmethod
    async def get_by_provider_id(self, user_provider_id: str) -> UserIdentity | None: ...
        
    @abstractmethod
    async def get_by_provider_id_with_user_and_roles(self, user_provider_id: str) -> UserIdentity | None: ...
       
    @abstractmethod
    async def add(self, user_identity: UserIdentity) -> UserIdentity: ...
       
