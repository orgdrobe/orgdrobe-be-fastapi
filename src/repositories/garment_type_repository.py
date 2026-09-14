from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import GarmentTypeRepositoryInterface
from repositories.generic_repository import GenericRepository
from models import GarmentType


class GarmentTypeRepository(GenericRepository[GarmentType], GarmentTypeRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, GarmentType)

