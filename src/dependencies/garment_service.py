from fastapi import Depends

from services import GarmentService
from services.interfaces import UnitOfWorkInterface, GarmentServiceInterface
from .unit_of_work import get_unit_of_work


def get_garment_service(uow: UnitOfWorkInterface = Depends(get_unit_of_work)) -> GarmentServiceInterface:
    return GarmentService(uow)

