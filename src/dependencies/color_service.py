from fastapi import Depends

from services import ColorService
from services.interfaces import UnitOfWorkInterface, ColorServiceInterface
from .unit_of_work import get_unit_of_work


def get_color_service(uow: UnitOfWorkInterface = Depends(get_unit_of_work)) -> ColorServiceInterface: 
    """Provide ColorService instance with Unit of Work dependency."""
    return ColorService(uow)

