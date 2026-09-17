from abc import ABC, abstractmethod

from models import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> User | None: ...
    
    @abstractmethod
    async def get_by_id_with_roles(self, id: int) -> User | None: ...
      
    @abstractmethod
    async def get_by_username(self, username: str) -> User | None: ...
       
    @abstractmethod
    async def get_by_email(self, email: str) ->  User | None: ...
    
    @abstractmethod 
    async def add(self, user: User) -> User: ...
  