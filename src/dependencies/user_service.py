from fastapi import Depends

from services import UserService
from services.interfaces import (
    MediaServiceInterface,
    UnitOfWorkInterface,
    UserServiceInterface,
)
from .media_service import get_media_service
from .unit_of_work import get_unit_of_work


def get_user_service(
    uow: UnitOfWorkInterface = Depends(get_unit_of_work),
    media_service: MediaServiceInterface = Depends(get_media_service),
) -> UserServiceInterface:
    """Provide UserService instance with Unit of Work and MediaService dependencies."""
    return UserService(uow=uow, media_service=media_service)

