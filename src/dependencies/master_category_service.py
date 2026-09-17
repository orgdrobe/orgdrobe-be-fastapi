from fastapi import Depends

from services import MasterCategoryService
from services.interfaces import UnitOfWorkInterface, MasterCategoryServiceInterface
from .unit_of_work import get_unit_of_work

def get_master_category_service(uow: UnitOfWorkInterface = Depends(get_unit_of_work)) -> MasterCategoryServiceInterface: 
    return MasterCategoryService(uow)