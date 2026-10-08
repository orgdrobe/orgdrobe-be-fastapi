from fastapi import Depends

from services import GarmentService
from services.interfaces import (
    GarmentServiceInterface,
    MediaServiceInterface,
    UnitOfWorkInterface,
)
from .media_service import get_media_service
from .unit_of_work import get_unit_of_work


def get_garment_service(
    uow: UnitOfWorkInterface = Depends(get_unit_of_work),
    media_service: MediaServiceInterface = Depends(get_media_service),
) -> GarmentServiceInterface:
    """Provide GarmentService instance with Unit of Work and MediaService dependencies."""
    return GarmentService(uow=uow, media_service=media_service)

