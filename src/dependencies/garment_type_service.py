from fastapi import Depends

from services import GarmentTypeService
from services.interfaces import UnitOfWorkInterface, GarmentTypeServiceInterface
from .unit_of_work import get_unit_of_work


def get_garment_type_service(uow: UnitOfWorkInterface = Depends(get_unit_of_work)) -> GarmentTypeServiceInterface: 
    return GarmentTypeService(uow)

