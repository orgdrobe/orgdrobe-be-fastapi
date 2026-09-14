import structlog

from core.exceptions.category_exceptions import SubCategoryNotFound
from schemas.sub_category import NewSubCategory, SubCategoryOut, UpdateSubCategory
from services.interfaces import UnitOfWorkInterface, SubCategoryServiceInterface
from repositories.interfaces import CategorySubRepositoryInterface
from models import CategorySub

logger = structlog.get_logger()

class SubCategoryService(SubCategoryServiceInterface):
    def __init__(self, uow: UnitOfWorkInterface) -> None:
        self._uow = uow 

    async def create(self, new_category_master: NewSubCategory) -> SubCategoryOut:
        logger.info("creating_sub_category", name=new_category_master.name)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(CategorySubRepositoryInterface)
            
            category_data = new_category_master.model_dump()
            category = CategorySub(**category_data)
            
            created_category = await repo.add(category)
            await uow.commit()
            
            result = SubCategoryOut.model_validate(created_category)
            logger.info("sub_category_created_successfully", category_id=result.id)
            
        return result

    async def get_by_id(self, id: int) -> SubCategoryOut:
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(CategorySubRepositoryInterface)
            
            category = await repo.get_by_id(id)
            if category is None:
                raise SubCategoryNotFound(id)

            result = SubCategoryOut.model_validate(category)
            
        return result

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[SubCategoryOut]:
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(CategorySubRepositoryInterface)
            
            categories = await repo.get_all(skip=skip, limit=limit)
            result = [SubCategoryOut.model_validate(cat) for cat in categories]
            
        return result

    async def update(self, id: int, update_data: UpdateSubCategory) -> SubCategoryOut:
        logger.info("updating_sub_category", category_id=id)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(CategorySubRepositoryInterface)
            
            category = await repo.get_by_id(id)
            if not category:
                logger.warning("sub_category_update_failed", reason="not_found", category_id=id)
                raise SubCategoryNotFound(id)
                
            data_dict = update_data.model_dump(exclude_unset=True)
            
            updated_category = await repo.update(category, data_dict)
            await uow.commit()
            
            result = SubCategoryOut.model_validate(updated_category)
            logger.info("sub_category_updated_successfully", category_id=result.id)
            
        return result

    async def delete(self, id: int) -> bool:
        logger.info("deleting_sub_category", category_id=id)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(CategorySubRepositoryInterface)
            
            is_deleted = await repo.delete(id)
            if not is_deleted:
                logger.warning("sub_category_delete_failed", reason="not_found", category_id=id)
                raise SubCategoryNotFound(id)
                
            await uow.commit()
            logger.info("sub_category_deleted_successfully", category_id=id)
            
        return True