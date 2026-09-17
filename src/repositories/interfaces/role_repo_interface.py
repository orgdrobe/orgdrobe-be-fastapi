from abc import ABC, abstractmethod

from models import Role

class RoleRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_name(self, role_name: str) -> Role | None: ... 