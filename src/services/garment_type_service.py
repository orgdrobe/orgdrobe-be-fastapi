import structlog

from core.exceptions.garment_type_exceptions import GarmentTypeNotFound
from schemas.garment_type import NewGarmentType, GarmentTypeOut, UpdateGarmentType
from services.interfaces import UnitOfWorkInterface, GarmentTypeServiceInterface
from repositories.interfaces import GarmentTypeRepositoryInterface
from models import GarmentType

logger = structlog.get_logger()


class GarmentTypeService(GarmentTypeServiceInterface):
    def __init__(self, uow: UnitOfWorkInterface) -> None:
        self._uow = uow 

    async def create(self, new_garment_type: NewGarmentType) -> GarmentTypeOut:
        logger.info("creating_garment_type", name=new_garment_type.name)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(GarmentTypeRepositoryInterface)
            
            garment_type_data = new_garment_type.model_dump()
            garment_type = GarmentType(**garment_type_data)
            
            created_garment_type = await repo.add(garment_type)
            await uow.commit()
            
            result = GarmentTypeOut.model_validate(created_garment_type)
            logger.info("garment_type_created_successfully", garment_type_id=result.id)
            
        return result

    async def get_by_id(self, id: int) -> GarmentTypeOut:
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(GarmentTypeRepositoryInterface)
            
            garment_type = await repo.get_by_id(id)
            if garment_type is None:
                raise GarmentTypeNotFound(id)

            result = GarmentTypeOut.model_validate(garment_type)
            
        return result

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[GarmentTypeOut]:
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(GarmentTypeRepositoryInterface)
            
            garment_types = await repo.get_all(skip=skip, limit=limit)
            result = [GarmentTypeOut.model_validate(gt) for gt in garment_types]
            
        return result

    async def update(self, id: int, update_data: UpdateGarmentType) -> GarmentTypeOut:
        logger.info("updating_garment_type", garment_type_id=id)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(GarmentTypeRepositoryInterface)
            
            garment_type = await repo.get_by_id(id)
            if not garment_type:
                logger.warning("garment_type_update_failed", reason="not_found", garment_type_id=id)
                raise GarmentTypeNotFound(id)
                
            data_dict = update_data.model_dump(exclude_unset=True)
            
            updated_garment_type = await repo.update(garment_type, data_dict)
            await uow.commit()
            
            result = GarmentTypeOut.model_validate(updated_garment_type)
            logger.info("garment_type_updated_successfully", garment_type_id=result.id)
            
        return result

    async def delete(self, id: int) -> bool:
        logger.info("deleting_garment_type", garment_type_id=id)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(GarmentTypeRepositoryInterface)
            
            is_deleted = await repo.delete(id)
            if not is_deleted:
                logger.warning("garment_type_delete_failed", reason="not_found", garment_type_id=id)
                raise GarmentTypeNotFound(id)
                
            await uow.commit()
            logger.info("garment_type_deleted_successfully", garment_type_id=id)
            
        return True

