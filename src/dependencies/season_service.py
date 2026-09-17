from fastapi import Depends

from services import SeasonService
from services.interfaces import UnitOfWorkInterface, SeasonServiceInterface
from .unit_of_work import get_unit_of_work


def get_season_service(uow: UnitOfWorkInterface = Depends(get_unit_of_work)) -> SeasonServiceInterface: 
    return SeasonService(uow)

