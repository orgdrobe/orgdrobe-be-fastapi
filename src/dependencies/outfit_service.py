from fastapi import Depends

from services import OutfitService
from services.interfaces import UnitOfWorkInterface, OutfitServiceInterface
from .unit_of_work import get_unit_of_work


def get_outfit_service(uow: UnitOfWorkInterface = Depends(get_unit_of_work)) -> OutfitServiceInterface:
    return OutfitService(uow)

