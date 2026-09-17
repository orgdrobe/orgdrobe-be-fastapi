from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import GenderRepositoryInterface
from repositories.generic_repository import GenericRepository
from models import Gender


class GenderRepository(GenericRepository[Gender], GenderRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Gender)

