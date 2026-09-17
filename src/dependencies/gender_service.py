from fastapi import Depends

from services import GenderService
from services.interfaces import UnitOfWorkInterface, GenderServiceInterface
from .unit_of_work import get_unit_of_work


def get_gender_service(uow: UnitOfWorkInterface = Depends(get_unit_of_work)) -> GenderServiceInterface: 
    return GenderService(uow)

