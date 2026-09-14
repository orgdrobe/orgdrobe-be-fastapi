from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import CategoryMasterRepositoryInterface
from repositories.generic_repository import GenericRepository
from models import CategoryMaster

class CategoryMasterRepository(GenericRepository[CategoryMaster], CategoryMasterRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, CategoryMaster)
