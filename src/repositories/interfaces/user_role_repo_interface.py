from abc import ABC, abstractmethod

from models import UserRole

class UserRoleRepositoryInterface(ABC):
    @abstractmethod
    async def add(self, user_role: UserRole) -> UserRole: ...