import structlog

from core.exceptions.category_exceptions import MasterCategoryNotFound
from schemas.master_category import NewMasterCategory, MasterCategoryOut, UpdateMasterCategory
from services.interfaces import UnitOfWorkInterface, MasterCategoryServiceInterface
from repositories.interfaces import CategoryMasterRepositoryInterface
from models import CategoryMaster

logger = structlog.get_logger()

class MasterCategoryService(MasterCategoryServiceInterface):
    def __init__(self, uow: UnitOfWorkInterface) -> None:
        self._uow = uow 

    async def create(self, new_category_master: NewMasterCategory) -> MasterCategoryOut:
        logger.info("creating_master_category", name=new_category_master.name)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(CategoryMasterRepositoryInterface)
            
            category_data = new_category_master.model_dump()
            category = CategoryMaster(**category_data)
            
            created_category = await repo.add(category)
            await uow.commit()
            
            result = MasterCategoryOut.model_validate(created_category)
            logger.info("master_category_created_successfully", category_id=result.id)
            
        return result

    async def get_by_id(self, id: int) -> MasterCategoryOut:
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(CategoryMasterRepositoryInterface)
            
            category = await repo.get_by_id(id)
            if category is None:
                raise MasterCategoryNotFound(id)

            result = MasterCategoryOut.model_validate(category)
            
        return result

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[MasterCategoryOut]:
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(CategoryMasterRepositoryInterface)
            
            categories = await repo.get_all(skip=skip, limit=limit)
            result = [MasterCategoryOut.model_validate(cat) for cat in categories]
            
        return result

    async def update(self, id: int, update_data: UpdateMasterCategory) -> MasterCategoryOut:
        logger.info("updating_master_category", category_id=id)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(CategoryMasterRepositoryInterface)
            
            category = await repo.get_by_id(id)
            if not category:
                logger.warning("master_category_update_failed", reason="not_found", category_id=id)
                raise MasterCategoryNotFound(id)
                
            data_dict = update_data.model_dump(exclude_unset=True)
            
            updated_category = await repo.update(category, data_dict)
            await uow.commit()
            
            result = MasterCategoryOut.model_validate(updated_category)
            logger.info("master_category_updated_successfully", category_id=result.id)
            
        return result

    async def delete(self, id: int) -> bool:
        logger.info("deleting_master_category", category_id=id)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(CategoryMasterRepositoryInterface)
            
            is_deleted = await repo.delete(id)
            if not is_deleted:
                logger.warning("master_category_delete_failed", reason="not_found", category_id=id)
                raise MasterCategoryNotFound(id)
                
            await uow.commit()
            logger.info("master_category_deleted_successfully", category_id=id)
            
        return True