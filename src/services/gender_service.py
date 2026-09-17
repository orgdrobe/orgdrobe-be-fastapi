import structlog

from core.exceptions.gender_exceptions import GenderNotFound
from schemas.gender import NewGender, GenderOut, UpdateGender
from services.interfaces import UnitOfWorkInterface, GenderServiceInterface
from repositories.interfaces import GenderRepositoryInterface
from models import Gender

logger = structlog.get_logger()


class GenderService(GenderServiceInterface):
    def __init__(self, uow: UnitOfWorkInterface) -> None:
        self._uow = uow 

    async def create(self, new_gender: NewGender) -> GenderOut:
        logger.info("creating_gender", name=new_gender.name)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(GenderRepositoryInterface)
            
            gender_data = new_gender.model_dump()
            gender = Gender(**gender_data)
            
            created_gender = await repo.add(gender)
            await uow.commit()
            
            result = GenderOut.model_validate(created_gender)
            logger.info("gender_created_successfully", gender_id=result.id)
            
        return result

    async def get_by_id(self, id: int) -> GenderOut:
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(GenderRepositoryInterface)
            
            gender = await repo.get_by_id(id)
            if gender is None:
                raise GenderNotFound(id)

            result = GenderOut.model_validate(gender)
            
        return result

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[GenderOut]:
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(GenderRepositoryInterface)
            
            genders = await repo.get_all(skip=skip, limit=limit)
            result = [GenderOut.model_validate(g) for g in genders]
            
        return result

    async def update(self, id: int, update_data: UpdateGender) -> GenderOut:
        logger.info("updating_gender", gender_id=id)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(GenderRepositoryInterface)
            
            gender = await repo.get_by_id(id)
            if not gender:
                logger.warning("gender_update_failed", reason="not_found", gender_id=id)
                raise GenderNotFound(id)
                
            data_dict = update_data.model_dump(exclude_unset=True)
            
            updated_gender = await repo.update(gender, data_dict)
            await uow.commit()
            
            result = GenderOut.model_validate(updated_gender)
            logger.info("gender_updated_successfully", gender_id=result.id)
            
        return result

    async def delete(self, id: int) -> bool:
        logger.info("deleting_gender", gender_id=id)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(GenderRepositoryInterface)
            
            is_deleted = await repo.delete(id)
            if not is_deleted:
                logger.warning("gender_delete_failed", reason="not_found", gender_id=id)
                raise GenderNotFound(id)
                
            await uow.commit()
            logger.info("gender_deleted_successfully", gender_id=id)
            
        return True

