from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import SeasonRepositoryInterface
from repositories.generic_repository import GenericRepository
from models import Season


class SeasonRepository(GenericRepository[Season], SeasonRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Season)

