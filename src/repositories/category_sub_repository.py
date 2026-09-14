from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import CategorySubRepositoryInterface
from repositories.generic_repository import GenericRepository
from models import CategorySub

class CategorySubRepository(GenericRepository[CategorySub], CategorySubRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, CategorySub)
