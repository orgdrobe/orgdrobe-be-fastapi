from typing import Any

import structlog

from core.exceptions.outfit_exceptions import OutfitNotFound, OutfitNameAlreadyExists
from core.exceptions.garment_exceptions import GarmentNotFound
from schemas.outfit import NewOutfit, UpdateOutfit, OutfitOut, OutfitColorOut
from schemas.garment import GarmentOut, GarmentColorOut
from schemas.gender import GenderOut
from schemas.master_category import MasterCategoryOut
from schemas.sub_category import SubCategoryOut
from schemas.garment_type import GarmentTypeOut
from schemas.season import SeasonOut
from schemas.usage import UsageOut
from services.interfaces import UnitOfWorkInterface, OutfitServiceInterface
from repositories.interfaces import (
    OutfitRepositoryInterface,
    ColorRepositoryInterface,
    GarmentRepositoryInterface
)
from models import Outfit, OutfitColor, Color, Garment

logger = structlog.get_logger()


class OutfitService(OutfitServiceInterface):
    def __init__(self, uow: UnitOfWorkInterface) -> None:
        self._uow = uow

    async def _resolve_colors(
        self,
        color_repo: ColorRepositoryInterface,
        colors_data: list[Any] | None,
    ) -> list[OutfitColor]:
        if not colors_data:
            return []
        resolved: list[OutfitColor] = []
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

            resolved.append(OutfitColor(color=color, is_primary=color_item.is_primary))
        return resolved

    async def _resolve_garments(
        self,
        garment_repo: GarmentRepositoryInterface,
        user_id: int,
        garment_ids: list[int] | None,
    ) -> list[Garment]:
        if not garment_ids:
            return []
        unique_ids = list(dict.fromkeys(garment_ids))
        existing_garments = await garment_repo.get_by_ids_and_user_id(
            ids=unique_ids,
            user_id=user_id
        )
        existing_ids = {g.id for g in existing_garments}
        missing_ids = [gid for gid in unique_ids if gid not in existing_ids]

        if missing_ids:
            logger.warning(
                "outfit_garments_not_found",
                user_id=user_id,
                missing_ids=missing_ids
            )
            raise GarmentNotFound(missing_ids if len(missing_ids) > 1 else missing_ids[0])

        return list(existing_garments)

    async def create(self, user_id: int, new_outfit: NewOutfit) -> OutfitOut:
        logger.info("creating_outfit", user_id=user_id, name=new_outfit.name)

        async with self._uow as uow:
            garment_repository = uow.get_repo_by_interface(GarmentRepositoryInterface)
            outfit_repository = uow.get_repo_by_interface(OutfitRepositoryInterface)
            color_repository = uow.get_repo_by_interface(ColorRepositoryInterface)

            if await outfit_repository.get_by_name(new_outfit.name):
                logger.warning("outfit_create_failed", reason="name_taken", name=new_outfit.name)
                raise OutfitNameAlreadyExists(new_outfit.name)

            garments = await self._resolve_garments(garment_repository, user_id, new_outfit.garment_ids)
            colors = await self._resolve_colors(color_repository, new_outfit.colors)

            outfit = Outfit(
                name=new_outfit.name,
                description=new_outfit.description,
                user_id=user_id,
                garments=garments,
                colors=colors,
            )
            outfit = await outfit_repository.add(outfit)
            await uow.commit()

            result = self._map_outfit_to_out(outfit)
            logger.info("outfit_created_successfully", outfit_id=result.id)

        return result

    async def get_by_id(self, user_id: int, id: int) -> OutfitOut:
        async with self._uow as uow:
            outfit_repository = uow.get_repo_by_interface(OutfitRepositoryInterface)

            outfit = await outfit_repository.get_by_id(id)
            if outfit is None or outfit.user_id != user_id:
                raise OutfitNotFound(id)

            result = self._map_outfit_to_out(outfit)

        return result

    async def get_all_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[OutfitOut]:
        async with self._uow as uow:
            outfit_repository = uow.get_repo_by_interface(OutfitRepositoryInterface)

            outfits = await outfit_repository.get_all_by_user_id(user_id=user_id, skip=skip, limit=limit)
            result = [self._map_outfit_to_out(o) for o in outfits]

        return result

    async def update(self, user_id: int, id: int, update_data: UpdateOutfit) -> OutfitOut:
        logger.info("updating_outfit", outfit_id=id, user_id=user_id)

        async with self._uow as uow:
            outfit_repository = uow.get_repo_by_interface(OutfitRepositoryInterface)
            garment_repository = uow.get_repo_by_interface(GarmentRepositoryInterface)
            color_repository = uow.get_repo_by_interface(ColorRepositoryInterface)

            outfit = await outfit_repository.get_by_id(id)
            if not outfit or outfit.user_id != user_id:
                logger.warning("outfit_update_failed", reason="not_found", outfit_id=id)
                raise OutfitNotFound(id)

            if update_data.name is not None and update_data.name != outfit.name:
                existing_outfit = await outfit_repository.get_by_name(update_data.name)
                if existing_outfit and existing_outfit.id != id:
                    logger.warning("outfit_update_failed", reason="name_taken", name=update_data.name)
                    raise OutfitNameAlreadyExists(update_data.name)

            data_dict = update_data.model_dump(exclude_unset=True, exclude={"garment_ids", "colors"})
            if data_dict:
                await outfit_repository.update(outfit, data_dict)

            if update_data.garment_ids is not None:
                outfit.garments = await self._resolve_garments(garment_repository, user_id, update_data.garment_ids)

            if update_data.colors is not None:
                outfit.colors = await self._resolve_colors(color_repository, update_data.colors)

            await uow.commit()

            result = self._map_outfit_to_out(outfit)
            logger.info("outfit_updated_successfully", outfit_id=result.id)

        return result

    async def delete(self, user_id: int, id: int) -> bool:
        logger.info("deleting_outfit", outfit_id=id, user_id=user_id)

        async with self._uow as uow:
            outfit_repository = uow.get_repo_by_interface(OutfitRepositoryInterface)

            outfit = await outfit_repository.get_by_id(id)
            if not outfit or outfit.user_id != user_id:
                logger.warning("outfit_delete_failed", reason="not_found", outfit_id=id)
                raise OutfitNotFound(id)

            is_deleted = await outfit_repository.delete(id)
            if not is_deleted:
                raise OutfitNotFound(id)

            await uow.commit()
            logger.info("outfit_deleted_successfully", outfit_id=id)

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

    def _map_outfit_to_out(self, outfit: Outfit) -> OutfitOut:
        garments_out = [
            self._map_garment_to_out(garment)
            for garment in (outfit.garments or [])
            if garment is not None
        ]
        colors_out = [
            OutfitColorOut(
                id=oc.color.id if oc.color else oc.color_id,
                red=oc.color.red if oc.color else 0,
                green=oc.color.green if oc.color else 0,
                blue=oc.color.blue if oc.color else 0,
                is_primary=oc.is_primary,
            )
            for oc in (outfit.colors or [])
            if oc.color is not None
        ]
        return OutfitOut(
            id=outfit.id,
            name=outfit.name,
            description=outfit.description,
            user_id=outfit.user_id,
            garments=garments_out,
            colors=colors_out,
        )

