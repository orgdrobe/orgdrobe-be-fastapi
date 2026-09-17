import structlog

from core.exceptions.season_exceptions import SeasonNotFound
from schemas.season import NewSeason, SeasonOut, UpdateSeason
from services.interfaces import UnitOfWorkInterface, SeasonServiceInterface
from repositories.interfaces import SeasonRepositoryInterface
from models import Season

logger = structlog.get_logger()


class SeasonService(SeasonServiceInterface):
    def __init__(self, uow: UnitOfWorkInterface) -> None:
        self._uow = uow 

    async def create(self, new_season: NewSeason) -> SeasonOut:
        logger.info("creating_season", name=new_season.name)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(SeasonRepositoryInterface)
            
            season_data = new_season.model_dump()
            season = Season(**season_data)
            
            created_season = await repo.add(season)
            await uow.commit()
            
            result = SeasonOut.model_validate(created_season)
            logger.info("season_created_successfully", season_id=result.id)
            
        return result

    async def get_by_id(self, id: int) -> SeasonOut:
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(SeasonRepositoryInterface)
            
            season = await repo.get_by_id(id)
            if season is None:
                raise SeasonNotFound(id)

            result = SeasonOut.model_validate(season)
            
        return result

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[SeasonOut]:
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(SeasonRepositoryInterface)
            
            seasons = await repo.get_all(skip=skip, limit=limit)
            result = [SeasonOut.model_validate(s) for s in seasons]
            
        return result

    async def update(self, id: int, update_data: UpdateSeason) -> SeasonOut:
        logger.info("updating_season", season_id=id)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(SeasonRepositoryInterface)
            
            season = await repo.get_by_id(id)
            if not season:
                logger.warning("season_update_failed", reason="not_found", season_id=id)
                raise SeasonNotFound(id)
                
            data_dict = update_data.model_dump(exclude_unset=True)
            
            updated_season = await repo.update(season, data_dict)
            await uow.commit()
            
            result = SeasonOut.model_validate(updated_season)
            logger.info("season_updated_successfully", season_id=result.id)
            
        return result

    async def delete(self, id: int) -> bool:
        logger.info("deleting_season", season_id=id)
        
        async with self._uow as uow:
            repo = uow.get_repo_by_interface(SeasonRepositoryInterface)
            
            is_deleted = await repo.delete(id)
            if not is_deleted:
                logger.warning("season_delete_failed", reason="not_found", season_id=id)
                raise SeasonNotFound(id)
                
            await uow.commit()
            logger.info("season_deleted_successfully", season_id=id)
            
        return True

