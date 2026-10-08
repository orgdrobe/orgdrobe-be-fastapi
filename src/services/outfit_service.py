import asyncio
from typing import Any

from fastapi import UploadFile
import structlog

from core.exceptions.outfit_exceptions import (
    OutfitNotFound,
    OutfitNameAlreadyExists,
    OutfitImageNotFound,
)
from core.exceptions.garment_exceptions import GarmentNotFound
from schemas.outfit import (
    NewOutfit,
    UpdateOutfit,
    OutfitOut,
    OutfitColorOut,
    OutfitImageOut,
)
from schemas.garment import GarmentOut, GarmentColorOut, GarmentImageOut
from schemas.gender import GenderOut
from schemas.master_category import MasterCategoryOut
from schemas.sub_category import SubCategoryOut
from schemas.garment_type import GarmentTypeOut
from schemas.season import SeasonOut
from schemas.usage import UsageOut
from services.interfaces import (
    UnitOfWorkInterface,
    OutfitServiceInterface,
    MediaServiceInterface,
)
from repositories.interfaces import (
    OutfitRepositoryInterface,
    OutfitImageRepositoryInterface,
    ColorRepositoryInterface,
    GarmentRepositoryInterface
)
from models import Outfit, OutfitColor, OutfitImage, Color, Garment

logger = structlog.get_logger()


class OutfitService(OutfitServiceInterface):
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        media_service: MediaServiceInterface | None = None,
    ) -> None:
        self._uow = uow
        self._media_service = media_service

    async def _resolve_colors(
        self,
        color_repo: ColorRepositoryInterface,
        colors_data: list[Any] | None,
    ) -> list[OutfitColor]:
        """Resolve or create Color models and link them via OutfitColor association."""
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
        """Verify garments exist, belong to user, and return garment models."""
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
        """Create a new outfit composed of garments and colors."""
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

            result = await self._map_outfit_to_out(outfit)
            logger.info("outfit_created_successfully", outfit_id=result.id)

        return result

    async def get_by_id(self, user_id: int, id: int) -> OutfitOut:
        """Retrieve an outfit by its ID ensuring user ownership."""
        async with self._uow as uow:
            outfit_repository = uow.get_repo_by_interface(OutfitRepositoryInterface)

            outfit = await outfit_repository.get_by_id(id)
            if outfit is None or outfit.user_id != user_id:
                raise OutfitNotFound(id)

            result = await self._map_outfit_to_out(outfit)

        return result

    async def get_all_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[OutfitOut]:
        """Retrieve a paginated list of outfits belonging to the user."""
        async with self._uow as uow:
            outfit_repository = uow.get_repo_by_interface(OutfitRepositoryInterface)

            outfits = await outfit_repository.get_all_by_user_id(user_id=user_id, skip=skip, limit=limit)
            result = [await self._map_outfit_to_out(o) for o in outfits]

        return result

    async def update(self, user_id: int, id: int, update_data: UpdateOutfit) -> OutfitOut:
        """Update outfit metadata, associated garments, and colors."""
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

            result = await self._map_outfit_to_out(outfit)
            logger.info("outfit_updated_successfully", outfit_id=result.id)

        return result

    async def delete(self, user_id: int, id: int) -> bool:
        """Delete a user outfit by ID and remove its images from media storage."""
        logger.info("deleting_outfit", outfit_id=id, user_id=user_id)

        async with self._uow as uow:
            outfit_repository = uow.get_repo_by_interface(OutfitRepositoryInterface)

            outfit = await outfit_repository.get_by_id(id)
            if not outfit or outfit.user_id != user_id:
                logger.warning("outfit_delete_failed", reason="not_found", outfit_id=id)
                raise OutfitNotFound(id)

            if self._media_service and outfit.images:
                for img in outfit.images:
                    await self._media_service.delete_media(user_id=user_id, file_key=img.image_key)

            is_deleted = await outfit_repository.delete(id)
            if not is_deleted:
                raise OutfitNotFound(id)

            await uow.commit()
            logger.info("outfit_deleted_successfully", outfit_id=id)

        return True

    async def add_image(
        self,
        user_id: int,
        outfit_id: int,
        file: UploadFile,
        is_primary: bool = False,
        order: int = 0,
    ) -> OutfitImageOut:
        """Upload, validate, and associate an image with an existing user outfit."""
        logger.info("adding_outfit_image", user_id=user_id, outfit_id=outfit_id)
        if not self._media_service:
            raise RuntimeError("MediaService is not configured")

        async with self._uow as uow:
            outfit_repo = uow.get_repo_by_interface(OutfitRepositoryInterface)
            outfit = await outfit_repo.get_by_id(outfit_id)
            if not outfit or outfit.user_id != user_id:
                raise OutfitNotFound(outfit_id)

            image_repo = uow.get_repo_by_interface(OutfitImageRepositoryInterface)
            existing_images = await image_repo.get_by_outfit_id(outfit_id)

            if is_primary:
                for img in existing_images:
                    if img.is_primary:
                        await image_repo.update(img, {"is_primary": False})
            elif not existing_images:
                is_primary = True

            uploaded = await self._media_service.upload_media(
                file=file,
                entity_type="outfits",
                entity_id=outfit_id,
                user_id=user_id,
            )

            new_image = OutfitImage(
                outfit_id=outfit_id,
                image_key=uploaded.file_key,
                is_primary=is_primary,
                order=order,
            )
            new_image = await image_repo.add(new_image)
            await uow.commit()

            return OutfitImageOut(
                id=new_image.id,
                outfit_id=new_image.outfit_id,
                image_key=new_image.image_key,
                url=uploaded.url,
                is_primary=new_image.is_primary,
                order=new_image.order,
                created_at=new_image.created_at,
            )

    async def delete_image(
        self, user_id: int, outfit_id: int, image_id: int
    ) -> bool:
        """Remove an outfit image from storage, cache, and database."""
        logger.info("deleting_outfit_image", user_id=user_id, outfit_id=outfit_id, image_id=image_id)
        if not self._media_service:
            raise RuntimeError("MediaService is not configured")

        async with self._uow as uow:
            outfit_repo = uow.get_repo_by_interface(OutfitRepositoryInterface)
            outfit = await outfit_repo.get_by_id(outfit_id)
            if not outfit or outfit.user_id != user_id:
                raise OutfitNotFound(outfit_id)

            image_repo = uow.get_repo_by_interface(OutfitImageRepositoryInterface)
            image = await image_repo.get_by_id(image_id)
            if not image or image.outfit_id != outfit_id:
                raise OutfitImageNotFound(image_id)

            await self._media_service.delete_media(
                user_id=user_id, file_key=image.image_key
            )
            await image_repo.delete(image_id)
            await uow.commit()
            return True

    async def add_images_batch(
        self, user_id: int, outfit_id: int, files: list[UploadFile]
    ) -> list[OutfitImageOut]:
        """Upload, validate, and associate multiple images with an existing outfit in batch."""
        logger.info("adding_outfit_images_batch", user_id=user_id, outfit_id=outfit_id, file_count=len(files))
        if not self._media_service:
            raise RuntimeError("MediaService is not configured")

        if not files:
            return []

        async with self._uow as uow:
            outfit_repo = uow.get_repo_by_interface(OutfitRepositoryInterface)
            outfit = await outfit_repo.get_by_id(outfit_id)
            if not outfit or outfit.user_id != user_id:
                logger.warning("outfit_batch_add_failed", reason="not_found_or_ownership", outfit_id=outfit_id)
                raise OutfitNotFound(outfit_id)

            image_repo = uow.get_repo_by_interface(OutfitImageRepositoryInterface)
            existing_images = await image_repo.get_by_outfit_id(outfit_id)
            base_order = len(existing_images)
            has_primary = any(img.is_primary for img in existing_images)

            # Upload files concurrently
            upload_tasks = [
                self._media_service.upload_media(
                    file=file,
                    entity_type="outfits",
                    entity_id=outfit_id,
                    user_id=user_id,
                )
                for file in files
            ]
            uploaded_results = await asyncio.gather(*upload_tasks)

            new_images: list[OutfitImageOut] = []
            for idx, uploaded in enumerate(uploaded_results):
                is_primary = not has_primary and idx == 0
                new_image = OutfitImage(
                    outfit_id=outfit_id,
                    image_key=uploaded.file_key,
                    is_primary=is_primary,
                    order=base_order + idx,
                )
                new_image = await image_repo.add(new_image)
                new_images.append(
                    OutfitImageOut(
                        id=new_image.id,
                        outfit_id=new_image.outfit_id,
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
        self, user_id: int, outfit_id: int, image_ids: list[int]
    ) -> bool:
        """Remove multiple outfit images from storage, cache, and database."""
        logger.info("deleting_outfit_images_batch", user_id=user_id, outfit_id=outfit_id, count=len(image_ids))
        if not self._media_service:
            raise RuntimeError("MediaService is not configured")

        if not image_ids:
            return True

        async with self._uow as uow:
            outfit_repo = uow.get_repo_by_interface(OutfitRepositoryInterface)
            outfit = await outfit_repo.get_by_id(outfit_id)
            if not outfit or outfit.user_id != user_id:
                raise OutfitNotFound(outfit_id)

            image_repo = uow.get_repo_by_interface(OutfitImageRepositoryInterface)
            images_to_delete: list[OutfitImage] = []
            for img_id in image_ids:
                img = await image_repo.get_by_id(img_id)
                if not img or img.outfit_id != outfit_id:
                    raise OutfitImageNotFound(img_id)
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

    async def _map_outfit_to_out(self, outfit: Outfit) -> OutfitOut:
        """Convert Outfit ORM model into OutfitOut schema with signed image URLs."""
        garments_out = [
            await self._map_garment_to_out(garment)
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

        images_out: list[OutfitImageOut] = []
        for img in (outfit.images or []):
            url = None
            if self._media_service:
                url = await self._media_service.get_presigned_url(
                    user_id=outfit.user_id, file_key=img.image_key
                )
            images_out.append(
                OutfitImageOut(
                    id=img.id,
                    outfit_id=img.outfit_id,
                    image_key=img.image_key,
                    url=url,
                    is_primary=img.is_primary,
                    order=img.order,
                    created_at=img.created_at,
                )
            )

        return OutfitOut(
            id=outfit.id,
            name=outfit.name,
            description=outfit.description,
            user_id=outfit.user_id,
            garments=garments_out,
            colors=colors_out,
            images=images_out,
        )


