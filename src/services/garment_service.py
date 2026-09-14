from typing import Any

import structlog

from core.exceptions.garment_exceptions import GarmentNotFound, GarmentNameAlreadyExists
from core.exceptions.gender_exceptions import GenderNotFound
from core.exceptions.category_exceptions import MasterCategoryNotFound, SubCategoryNotFound
from core.exceptions.garment_type_exceptions import GarmentTypeNotFound
from core.exceptions.season_exceptions import SeasonNotFound
from core.exceptions.usage_exceptions import UsageNotFound
from schemas.garment import NewGarment, UpdateGarment, GarmentOut, GarmentColorOut
from schemas.gender import GenderOut
from schemas.master_category import MasterCategoryOut
from schemas.sub_category import SubCategoryOut
from schemas.garment_type import GarmentTypeOut
from schemas.season import SeasonOut
from schemas.usage import UsageOut
from services.interfaces import UnitOfWorkInterface, GarmentServiceInterface
from repositories.interfaces import (
    GarmentRepositoryInterface,
    ColorRepositoryInterface,
    GenderRepositoryInterface,
    CategoryMasterRepositoryInterface,
    CategorySubRepositoryInterface,
    GarmentTypeRepositoryInterface,
    SeasonRepositoryInterface,
    UsageRepositoryInterface
)
from models import (
    Garment,
    GarmentColor,
    Color,
    Gender,
    CategoryMaster,
    CategorySub,
    GarmentType,
    Season,
    Usage
)

logger = structlog.get_logger()

class GarmentService(GarmentServiceInterface):
    def __init__(self, uow: UnitOfWorkInterface) -> None:
        self._uow = uow 

    async def _validate_and_get_foreign_keys(
        self,
        uow: UnitOfWorkInterface,
        gender_id: int | None = None,
        category_master_id: int | None = None,
        category_sub_id: int | None = None,
        garment_type_id: int | None = None,
        season_id: int | None = None,
        usage_id: int | None = None
    ) -> tuple[Gender | None, CategoryMaster | None, CategorySub | None, GarmentType | None, Season | None, Usage | None]:
        gender = None
        if gender_id is not None:
            gender_repo = uow.get_repo_by_interface(GenderRepositoryInterface)
            gender = await gender_repo.get_by_id(gender_id)
            if not gender:
                raise GenderNotFound(gender_id)

        category_master = None
        if category_master_id is not None:
            master_repo = uow.get_repo_by_interface(CategoryMasterRepositoryInterface)
            category_master = await master_repo.get_by_id(category_master_id)
            if not category_master:
                raise MasterCategoryNotFound(category_master_id)

        category_sub = None
        if category_sub_id is not None:
            sub_repo = uow.get_repo_by_interface(CategorySubRepositoryInterface)
            category_sub = await sub_repo.get_by_id(category_sub_id)
            if not category_sub:
                raise SubCategoryNotFound(category_sub_id)

        garment_type = None
        if garment_type_id is not None:
            type_repo = uow.get_repo_by_interface(GarmentTypeRepositoryInterface)
            garment_type = await type_repo.get_by_id(garment_type_id)
            if not garment_type:
                raise GarmentTypeNotFound(garment_type_id)

        season = None
        if season_id is not None:
            season_repo = uow.get_repo_by_interface(SeasonRepositoryInterface)
            season = await season_repo.get_by_id(season_id)
            if not season:
                raise SeasonNotFound(season_id)

        usage = None
        if usage_id is not None:
            usage_repo = uow.get_repo_by_interface(UsageRepositoryInterface)
            usage = await usage_repo.get_by_id(usage_id)
            if not usage:
                raise UsageNotFound(usage_id)

        return gender, category_master, category_sub, garment_type, season, usage

    async def _resolve_colors(
        self,
        color_repo: ColorRepositoryInterface,
        colors_data: list[Any] | None,
    ) -> list[GarmentColor]:
        if not colors_data:
            return []
        resolved: list[GarmentColor] = []
        seen_rgb: set[tuple[int, int, int]] = set()
        seen_color_ids: set[int] = set()
        for color_item in colors_data:
            rgb = (color_item.red, color_item.green, color_item.blue)
            if rgb in seen_rgb:
                continue
            seen_rgb.add(rgb)

            color = await color_repo.get_by_rgb(color_item.red, color_item.green, color_item.blue)
            if not color:
                color = Color(red=color_item.red, green=color_item.green, blue=color_item.blue)
                color = await color_repo.add(color)

            if color.id and color.id in seen_color_ids:
                continue
            if color.id:
                seen_color_ids.add(color.id)

            resolved.append(GarmentColor(color=color, is_primary=color_item.is_primary))
        return resolved

    async def create(self, user_id: int, new_garment: NewGarment) -> GarmentOut:
        logger.info("creating_garment", user_id=user_id, name=new_garment.name)
        
        async with self._uow as uow:
            garment_repository = uow.get_repo_by_interface(GarmentRepositoryInterface)
            if await garment_repository.get_by_name(new_garment.name):
                logger.warning("garment_create_failed", reason="name_taken", name=new_garment.name)
                raise GarmentNameAlreadyExists(new_garment.name)

            (
                gender,
                category_master,
                category_sub,
                garment_type,
                season,
                usage,
            ) = await self._validate_and_get_foreign_keys(
                uow=uow,
                gender_id=new_garment.gender_id,
                category_master_id=new_garment.category_master_id,
                category_sub_id=new_garment.category_sub_id,
                garment_type_id=new_garment.garment_type_id,
                season_id=new_garment.season_id,
                usage_id=new_garment.usage_id,
            )

            color_repository = uow.get_repo_by_interface(ColorRepositoryInterface)
            
            colors = await self._resolve_colors(color_repository, new_garment.colors)

            garment = Garment(
                name=new_garment.name,
                description=new_garment.description,
                user_id=user_id,
                gender=gender,
                category_master=category_master,
                category_sub=category_sub,
                garment_type=garment_type,
                season=season,
                usage=usage,
                colors=colors,
            )
            garment = await garment_repository.add(garment)
            await uow.commit()
            
            result = self._map_garment_to_out(garment)
            logger.info("garment_created_successfully", garment_id=result.id)
            
        return result

    async def get_by_id(self, user_id: int, id: int) -> GarmentOut:
        async with self._uow as uow:
            garment_repository = uow.get_repo_by_interface(GarmentRepositoryInterface)
            
            garment = await garment_repository.get_by_id(id)
            if garment is None or garment.user_id != user_id:
                logger.warning("garment_get_failed", reason="not_found_or_wrong_ownership", garment_id=id)
                raise GarmentNotFound(id)

            result = self._map_garment_to_out(garment)
            
        return result

    async def get_all_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[GarmentOut]:
        async with self._uow as uow:
            garment_repository = uow.get_repo_by_interface(GarmentRepositoryInterface)
            
            garments = await garment_repository.get_all_by_user_id(user_id=user_id, skip=skip, limit=limit)
            result = [self._map_garment_to_out(g) for g in garments]
            
        return result

    async def update(self, user_id: int, id: int, update_data: UpdateGarment) -> GarmentOut:
        logger.info("updating_garment", garment_id=id, user_id=user_id)
        
        async with self._uow as uow:
            garment_repository = uow.get_repo_by_interface(GarmentRepositoryInterface)
            color_repository = uow.get_repo_by_interface(ColorRepositoryInterface)
            
            garment = await garment_repository.get_by_id(id)
            if not garment or garment.user_id != user_id:
                logger.warning("garment_update_failed", reason="not_found_or_wrong_ownership", garment_id=id)
                raise GarmentNotFound(id)

            if update_data.name is not None and update_data.name != garment.name:
                existing_garment = await garment_repository.get_by_name(update_data.name)
                if existing_garment and existing_garment.id != id:
                    logger.warning("garment_update_failed", reason="name_taken", name=update_data.name)
                    raise GarmentNameAlreadyExists(update_data.name)

            (
                gender,
                category_master,
                category_sub,
                garment_type,
                season,
                usage,
            ) = await self._validate_and_get_foreign_keys(
                uow=uow,
                gender_id=update_data.gender_id,
                category_master_id=update_data.category_master_id,
                category_sub_id=update_data.category_sub_id,
                garment_type_id=update_data.garment_type_id,
                season_id=update_data.season_id,
                usage_id=update_data.usage_id,
            )
                
            data_dict = update_data.model_dump(
                exclude_unset=True,
                exclude={"colors", "gender_id", "category_master_id", "category_sub_id", "garment_type_id", "season_id", "usage_id"}
            )
            if data_dict:
                await garment_repository.update(garment, data_dict)

            if gender is not None:
                garment.gender = gender
            if category_master is not None:
                garment.category_master = category_master
            if category_sub is not None:
                garment.category_sub = category_sub
            if garment_type is not None:
                garment.garment_type = garment_type
            if season is not None:
                garment.season = season
            if usage is not None:
                garment.usage = usage

            if update_data.colors is not None:
                garment.colors = await self._resolve_colors(color_repository, update_data.colors)

            await uow.commit()
            
            result = self._map_garment_to_out(garment)
            logger.info("garment_updated_successfully", garment_id=result.id)
            
        return result

    async def delete(self, user_id: int, id: int) -> bool:
        logger.info("deleting_garment", garment_id=id, user_id=user_id)
        
        async with self._uow as uow:
            garment_repository = uow.get_repo_by_interface(GarmentRepositoryInterface)
            
            garment = await garment_repository.get_by_id(id)
            if not garment or garment.user_id != user_id:
                logger.warning("garment_delete_failed", reason="not_found", garment_id=id)
                raise GarmentNotFound(id)
                
            is_deleted = await garment_repository.delete(id)
            if not is_deleted:
                raise GarmentNotFound(id)
                
            await uow.commit()
            logger.info("garment_deleted_successfully", garment_id=id)
            
        return True

    def _map_garment_to_out(self, garment: Garment) -> GarmentOut:
        colors_out = [
            GarmentColorOut(
                id=gc.color.id if gc.color else gc.color_id,
                red=gc.color.red if gc.color else 0,
                green=gc.color.green if gc.color else 0,
                blue=gc.color.blue if gc.color else 0,
                is_primary=gc.is_primary,
            )
            for gc in (garment.colors or [])
            if gc.color is not None
        ]
        return GarmentOut(
            id=garment.id,
            name=garment.name,
            description=garment.description,
            user_id=garment.user_id,
            gender=GenderOut.model_validate(garment.gender),
            category_master=MasterCategoryOut.model_validate(garment.category_master),
            category_sub=SubCategoryOut.model_validate(garment.category_sub),
            garment_type=GarmentTypeOut.model_validate(garment.garment_type),
            season=SeasonOut.model_validate(garment.season),
            usage=UsageOut.model_validate(garment.usage),
            colors=colors_out,
        )
