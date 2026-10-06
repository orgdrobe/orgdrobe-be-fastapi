from fastapi import Depends

from services import MasterCategoryService
from services.interfaces import UnitOfWorkInterface, MasterCategoryServiceInterface
from .unit_of_work import get_unit_of_work

def get_master_category_service(uow: UnitOfWorkInterface = Depends(get_unit_of_work)) -> MasterCategoryServiceInterface: 
    """Provide MasterCategoryService instance with Unit of Work dependency."""
    return MasterCategoryService(uow)