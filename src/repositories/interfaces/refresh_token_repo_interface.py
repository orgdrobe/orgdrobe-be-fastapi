from uuid import UUID
from abc import ABC, abstractmethod

from models import RefreshToken

class RefreshTokenRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_jti(self, jti: UUID) -> RefreshToken | None: ...

    @abstractmethod
    async def get_by_jti_with_user_and_roles(self, jti: UUID) -> RefreshToken | None: ...

    @abstractmethod
    async def add(self, refresh_token: RefreshToken) -> RefreshToken: ...
