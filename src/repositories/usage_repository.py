from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import UsageRepositoryInterface
from repositories.generic_repository import GenericRepository
from models import Usage


class UsageRepository(GenericRepository[Usage], UsageRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Usage)

