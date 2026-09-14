import structlog

from core.exceptions.usage_exceptions import UsageNotFound
from schemas.usage import NewUsage, UsageOut, UpdateUsage
from services.interfaces import UnitOfWorkInterface, UsageServiceInterface
from repositories.interfaces import UsageRepositoryInterface
from models import Usage

logger = structlog.get_logger()


class UsageService(UsageServiceInterface):
    def __init__(self, uow: UnitOfWorkInterface) -> None:
        self._uow = uow 

    async def create(self, new_usage: NewUsage) -> UsageOut:
        logger.info("creating_usage", name=new_usage.name)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(UsageRepositoryInterface)
            
            usage_data = new_usage.model_dump()
            usage = Usage(**usage_data)
            
            created_usage = await repo.add(usage)
            await uow.commit()
            
            result = UsageOut.model_validate(created_usage)
            logger.info("usage_created_successfully", usage_id=result.id)
            
        return result

    async def get_by_id(self, id: int) -> UsageOut:
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(UsageRepositoryInterface)
            
            usage = await repo.get_by_id(id)
            if usage is None:
                raise UsageNotFound(id)

            result = UsageOut.model_validate(usage)
            
        return result

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[UsageOut]:
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(UsageRepositoryInterface)
            
            uses = await repo.get_all(skip=skip, limit=limit)
            result = [UsageOut.model_validate(u) for u in uses]
            
        return result

    async def update(self, id: int, update_data: UpdateUsage) -> UsageOut:
        logger.info("updating_usage", usage_id=id)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(UsageRepositoryInterface)
            
            usage = await repo.get_by_id(id)
            if not usage:
                logger.warning("usage_update_failed", reason="not_found", usage_id=id)
                raise UsageNotFound(id)
                
            data_dict = update_data.model_dump(exclude_unset=True)
            
            updated_usage = await repo.update(usage, data_dict)
            await uow.commit()
            
            result = UsageOut.model_validate(updated_usage)
            logger.info("usage_updated_successfully", usage_id=result.id)
            
        return result

    async def delete(self, id: int) -> bool:
        logger.info("deleting_usage", usage_id=id)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(UsageRepositoryInterface)
            
            is_deleted = await repo.delete(id)
            if not is_deleted:
                logger.warning("usage_delete_failed", reason="not_found", usage_id=id)
                raise UsageNotFound(id)
                
            await uow.commit()
            logger.info("usage_deleted_successfully", usage_id=id)
            
        return True

