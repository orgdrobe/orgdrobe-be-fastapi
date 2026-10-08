import asyncio
from typing import Any

from fastapi import UploadFile
import structlog

from core.exceptions.garment_exceptions import (
    GarmentNotFound,
    GarmentNameAlreadyExists,
    GarmentImageNotFound,
)
from core.exceptions.gender_exceptions import GenderNotFound
from core.exceptions.category_exceptions import MasterCategoryNotFound, SubCategoryNotFound
from core.exceptions.garment_type_exceptions import GarmentTypeNotFound
from core.exceptions.season_exceptions import SeasonNotFound
from core.exceptions.usage_exceptions import UsageNotFound
from schemas.garment import (
    NewGarment,
    UpdateGarment,
    GarmentOut,
    GarmentColorOut,
    GarmentImageOut,
)
from schemas.gender import GenderOut
from schemas.master_category import MasterCategoryOut
from schemas.sub_category import SubCategoryOut
from schemas.garment_type import GarmentTypeOut
from schemas.season import SeasonOut
from schemas.usage import UsageOut
from services.interfaces import (
    UnitOfWorkInterface,
    GarmentServiceInterface,
    MediaServiceInterface,
)
from repositories.interfaces import (
    GarmentRepositoryInterface,
    GarmentImageRepositoryInterface,
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
    GarmentImage,
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
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        media_service: MediaServiceInterface | None = None,
    ) -> None:
        self._uow = uow
        self._media_service = media_service 

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
        """Validate and retrieve foreign key entity models for a garment."""
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
        """Resolve or create Color models and link them via GarmentColor association."""
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
        """Create a new garment for the specified user after validating foreign keys."""
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
            
            result = await self._map_garment_to_out(garment)
            logger.info("garment_created_successfully", garment_id=result.id)
            
        return result

    async def get_by_id(self, user_id: int, id: int) -> GarmentOut:
        """Retrieve a garment by its ID ensuring user ownership."""
        async with self._uow as uow:
            garment_repository = uow.get_repo_by_interface(GarmentRepositoryInterface)
            
            garment = await garment_repository.get_by_id(id)
            if garment is None or garment.user_id != user_id:
                logger.warning("garment_get_failed", reason="not_found_or_wrong_ownership", garment_id=id)
                raise GarmentNotFound(id)

            result = await self._map_garment_to_out(garment)
            
        return result

    async def get_all_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[GarmentOut]:
        """Retrieve a paginated list of garments belonging to the user."""
        async with self._uow as uow:
            garment_repository = uow.get_repo_by_interface(GarmentRepositoryInterface)
            
            garments = await garment_repository.get_all_by_user_id(user_id=user_id, skip=skip, limit=limit)
            result = [await self._map_garment_to_out(g) for g in garments]
            
        return result

    async def update(self, user_id: int, id: int, update_data: UpdateGarment) -> GarmentOut:
        """Update fields, relationships, and colors of an existing user garment."""
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
            
            result = await self._map_garment_to_out(garment)
            logger.info("garment_updated_successfully", garment_id=result.id)
            
        return result

    async def delete(self, user_id: int, id: int) -> bool:
        """Delete a user garment by ID and remove its images from media storage."""
        logger.info("deleting_garment", garment_id=id, user_id=user_id)
        
        async with self._uow as uow:
            garment_repository = uow.get_repo_by_interface(GarmentRepositoryInterface)
            
            garment = await garment_repository.get_by_id(id)
            if not garment or garment.user_id != user_id:
                logger.warning("garment_delete_failed", reason="not_found", garment_id=id)
                raise GarmentNotFound(id)

            if self._media_service and garment.images:
                for img in garment.images:
                    await self._media_service.delete_media(user_id=user_id, file_key=img.image_key)
                
            is_deleted = await garment_repository.delete(id)
            if not is_deleted:
                raise GarmentNotFound(id)
                
            await uow.commit()
            logger.info("garment_deleted_successfully", garment_id=id)
            
        return True

    async def add_image(
        self,
        user_id: int,
        garment_id: int,
        file: UploadFile,
        is_primary: bool = False,
        order: int = 0,
    ) -> GarmentImageOut:
        """Upload, validate, and associate an image with an existing user garment."""
        logger.info("adding_garment_image", user_id=user_id, garment_id=garment_id)
        if not self._media_service:
            raise RuntimeError("MediaService is not configured")

        async with self._uow as uow:
            garment_repo = uow.get_repo_by_interface(GarmentRepositoryInterface)
            garment = await garment_repo.get_by_id(garment_id)
            if not garment or garment.user_id != user_id:
                logger.warning("garment_add_image_failed", reason="not_found_or_ownership", garment_id=garment_id)
                raise GarmentNotFound(garment_id)

            image_repo = uow.get_repo_by_interface(GarmentImageRepositoryInterface)
            existing_images = await image_repo.get_by_garment_id(garment_id)

            if is_primary:
                for img in existing_images:
                    if img.is_primary:
                        await image_repo.update(img, {"is_primary": False})
            elif not existing_images:
                is_primary = True

            uploaded = await self._media_service.upload_media(
                file=file,
                entity_type="garments",
                entity_id=garment_id,
                user_id=user_id,
            )

            new_image = GarmentImage(
                garment_id=garment_id,
                image_key=uploaded.file_key,
                is_primary=is_primary,
                order=order,
            )
            new_image = await image_repo.add(new_image)
            await uow.commit()

            return GarmentImageOut(
                id=new_image.id,
                garment_id=new_image.garment_id,
                image_key=new_image.image_key,
                url=uploaded.url,
                is_primary=new_image.is_primary,
                order=new_image.order,
                created_at=new_image.created_at,
            )

    async def delete_image(
        self, user_id: int, garment_id: int, image_id: int
    ) -> bool:
        """Remove a garment image from storage, cache, and database."""
        logger.info("deleting_garment_image", user_id=user_id, garment_id=garment_id, image_id=image_id)
        if not self._media_service:
            raise RuntimeError("MediaService is not configured")

        async with self._uow as uow:
            garment_repo = uow.get_repo_by_interface(GarmentRepositoryInterface)
            garment = await garment_repo.get_by_id(garment_id)
            if not garment or garment.user_id != user_id:
                raise GarmentNotFound(garment_id)

            image_repo = uow.get_repo_by_interface(GarmentImageRepositoryInterface)
            image = await image_repo.get_by_id(image_id)
            if not image or image.garment_id != garment_id:
                raise GarmentImageNotFound(image_id)

            await self._media_service.delete_media(
                user_id=user_id, file_key=image.image_key
            )
            await image_repo.delete(image_id)
            await uow.commit()
            return True

    async def add_images_batch(
        self, user_id: int, garment_id: int, files: list[UploadFile]
    ) -> list[GarmentImageOut]:
        """Upload, validate, and associate multiple images with an existing garment in batch."""
        logger.info("adding_garment_images_batch", user_id=user_id, garment_id=garment_id, file_count=len(files))
        if not self._media_service:
            raise RuntimeError("MediaService is not configured")

        if not files:
            return []

        async with self._uow as uow:
            garment_repo = uow.get_repo_by_interface(GarmentRepositoryInterface)
            garment = await garment_repo.get_by_id(garment_id)
            if not garment or garment.user_id != user_id:
                logger.warning("garment_batch_add_failed", reason="not_found_or_ownership", garment_id=garment_id)
                raise GarmentNotFound(garment_id)

            image_repo = uow.get_repo_by_interface(GarmentImageRepositoryInterface)
            existing_images = await image_repo.get_by_garment_id(garment_id)
            base_order = len(existing_images)
            has_primary = any(img.is_primary for img in existing_images)

            # Upload files concurrently
            upload_tasks = [
                self._media_service.upload_media(
                    file=file,
                    entity_type="garments",
                    entity_id=garment_id,
                    user_id=user_id,
                )
                for file in files
            ]
            uploaded_results = await asyncio.gather(*upload_tasks)

            new_images: list[GarmentImageOut] = []
            for idx, uploaded in enumerate(uploaded_results):
                is_primary = not has_primary and idx == 0
                new_image = GarmentImage(
                    garment_id=garment_id,
                    image_key=uploaded.file_key,
                    is_primary=is_primary,
                    order=base_order + idx,
                )
                new_image = await image_repo.add(new_image)
                new_images.append(
                    GarmentImageOut(
                        id=new_image.id,
                        garment_id=new_image.garment_id,
                        image_key=new_image.image_key,
                        url=uploaded.url,
                        is_primary=new_image.is_primary,
                        order=new_image.order,
                        created_at=new_image.created_at,
                    )
                )

            await uow.commit()
            return new_images

    async def delete_images_batch(
        self, user_id: int, garment_id: int, image_ids: list[int]
    ) -> bool:
        """Remove multiple garment images from storage, cache, and database."""
        logger.info("deleting_garment_images_batch", user_id=user_id, garment_id=garment_id, count=len(image_ids))
        if not self._media_service:
            raise RuntimeError("MediaService is not configured")

        if not image_ids:
            return True

        async with self._uow as uow:
            garment_repo = uow.get_repo_by_interface(GarmentRepositoryInterface)
            garment = await garment_repo.get_by_id(garment_id)
            if not garment or garment.user_id != user_id:
                raise GarmentNotFound(garment_id)

            image_repo = uow.get_repo_by_interface(GarmentImageRepositoryInterface)
            images_to_delete: list[GarmentImage] = []
            for img_id in image_ids:
                img = await image_repo.get_by_id(img_id)
                if not img or img.garment_id != garment_id:
                    raise GarmentImageNotFound(img_id)
                images_to_delete.append(img)

            # Delete from S3 and cache concurrently
            delete_tasks = [
                self._media_service.delete_media(
                    user_id=user_id, file_key=img.image_key
                )
                for img in images_to_delete
            ]
            await asyncio.gather(*delete_tasks)

            for img in images_to_delete:
                await image_repo.delete(img.id)

            await uow.commit()
            return True

    async def _map_garment_to_out(self, garment: Garment) -> GarmentOut:
        """Convert Garment ORM model into GarmentOut schema with signed image URLs."""
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

        images_out: list[GarmentImageOut] = []
        for img in (garment.images or []):
            url = None
            if self._media_service:
                url = await self._media_service.get_presigned_url(
                    user_id=garment.user_id, file_key=img.image_key
                )
            images_out.append(
                GarmentImageOut(
                    id=img.id,
                    garment_id=img.garment_id,
                    image_key=img.image_key,
                    url=url,
                    is_primary=img.is_primary,
                    order=img.order,
                    created_at=img.created_at,
                )
            )

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
            images=images_out,
        )
