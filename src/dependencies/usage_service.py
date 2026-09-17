from fastapi import Depends

from services import UsageService
from services.interfaces import UnitOfWorkInterface, UsageServiceInterface
from .unit_of_work import get_unit_of_work


def get_usage_service(uow: UnitOfWorkInterface = Depends(get_unit_of_work)) -> UsageServiceInterface: 
    return UsageService(uow)

