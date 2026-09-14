from fastapi import Depends

from services import SubCategoryService
from services.interfaces import UnitOfWorkInterface, SubCategoryServiceInterface
from .unit_of_work import get_unit_of_work

def get_sub_category_service(uow: UnitOfWorkInterface = Depends(get_unit_of_work)) -> SubCategoryServiceInterface: 
    return SubCategoryService(uow)