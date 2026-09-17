from fastapi import Depends
from passlib.context import CryptContext

from services import AuthService
from services.interfaces import AuthServiceInterface, UnitOfWorkInterface, CacheServiceInterface
from .unit_of_work import get_unit_of_work
from .password_context import get_pwd_context
from .cache_service import get_cache_service

def get_auth_service(uow: UnitOfWorkInterface = Depends(get_unit_of_work), cache_service: CacheServiceInterface = Depends(get_cache_service), pwd_context: CryptContext = Depends(get_pwd_context)) -> AuthServiceInterface: 
    cache_service.prefix = "auth"
    return AuthService(uow, cache_service, pwd_context)