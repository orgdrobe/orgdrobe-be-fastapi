import structlog

from core.exceptions.color_exceptions import ColorNotFound
from schemas.color import NewColor, ColorOut, UpdateColor
from services.interfaces import UnitOfWorkInterface, ColorServiceInterface
from repositories.interfaces import ColorRepositoryInterface
from models import Color

logger = structlog.get_logger()


class ColorService(ColorServiceInterface):
    def __init__(self, uow: UnitOfWorkInterface) -> None:
        self._uow = uow 

    async def create(self, new_color: NewColor) -> ColorOut:
        logger.info("creating_color", red=new_color.red, green=new_color.green, blue=new_color.blue)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(ColorRepositoryInterface)
            
            color_data = new_color.model_dump()
            color = Color(**color_data)
            
            created_color = await repo.add(color)
            await uow.commit()
            
            result = ColorOut.model_validate(created_color)
            logger.info("color_created_successfully", color_id=result.id)
            
        return result

    async def get_by_id(self, id: int) -> ColorOut:
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(ColorRepositoryInterface)
            
            color = await repo.get_by_id(id)
            if color is None:
                raise ColorNotFound(id)

            result = ColorOut.model_validate(color)
            
        return result

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ColorOut]:
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(ColorRepositoryInterface)
            
            colors = await repo.get_all(skip=skip, limit=limit)
            result = [ColorOut.model_validate(c) for c in colors]
            
        return result

    async def update(self, id: int, update_data: UpdateColor) -> ColorOut:
        logger.info("updating_color", color_id=id)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(ColorRepositoryInterface)
            
            color = await repo.get_by_id(id)
            if not color:
                logger.warning("color_update_failed", reason="not_found", color_id=id)
                raise ColorNotFound(id)
                
            data_dict = update_data.model_dump(exclude_unset=True)
            
            updated_color = await repo.update(color, data_dict)
            await uow.commit()
            
            result = ColorOut.model_validate(updated_color)
            logger.info("color_updated_successfully", color_id=result.id)
            
        return result

    async def delete(self, id: int) -> bool:
        logger.info("deleting_color", color_id=id)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(ColorRepositoryInterface)
            
            is_deleted = await repo.delete(id)
            if not is_deleted:
                logger.warning("color_delete_failed", reason="not_found", color_id=id)
                raise ColorNotFound(id)
                
            await uow.commit()
            logger.info("color_deleted_successfully", color_id=id)
            
        return True

