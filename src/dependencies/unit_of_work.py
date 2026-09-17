from core.database.database_context import async_session_factory
from services import SqlAlchemyUnitOfWork
from services.interfaces import UnitOfWorkInterface
from repositories import UserRepository, UserIdentityRepository, UserRoleRepository, RoleRepository, RefreshTokenRepository
from repositories.interfaces import (UserIdentityRepositoryInterface, UserRepositoryInterface, RoleRepositoryInterface,
                                     UserRoleRepositoryInterface, RefreshTokenRepositoryInterface)


def get_unit_of_work() -> UnitOfWorkInterface:
    unit_of_work = SqlAlchemyUnitOfWork(session_factory=async_session_factory)
    
    unit_of_work.register_factory_by_interface(UserRepositoryInterface, lambda session: UserRepository(session))
    unit_of_work.register_factory_by_interface(UserIdentityRepositoryInterface, lambda session: UserIdentityRepository(session))
    unit_of_work.register_factory_by_interface(RoleRepositoryInterface, lambda session: RoleRepository(session))
    unit_of_work.register_factory_by_interface(UserRoleRepositoryInterface, lambda session: UserRoleRepository(session))
    unit_of_work.register_factory_by_interface(RefreshTokenRepositoryInterface, lambda session: RefreshTokenRepository(session))


    return unit_of_work