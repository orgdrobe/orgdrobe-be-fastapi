from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from schemas.garment import GarmentImageOut, GarmentOut, NewGarment, UpdateGarment
from schemas.media import BatchDeleteImagesRequest
from services.interfaces import GarmentServiceInterface
from schemas.errors import ErrorResponse
from dependencies import get_garment_service, get_current_user
from models import User

router = APIRouter()


@router.get(
    "/",
    response_model=list[GarmentOut],
    status_code=status.HTTP_200_OK,
)
async def garments_all_by_user(
    garment_service: Annotated[GarmentServiceInterface, Depends(get_garment_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100
) -> list[GarmentOut]:
    return await garment_service.get_all_by_user_id(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )


@router.get(
    "/{id}",
    response_model=GarmentOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Garment not found"},
    }
)
async def garment_by_id(
    id: int,
    garment_service: Annotated[GarmentServiceInterface, Depends(get_garment_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> GarmentOut:
    return await garment_service.get_by_id(user_id=current_user.id, id=id)


@router.post(
    "/",
    response_model=GarmentOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"model": ErrorResponse, "description": "Referenced entity not found"},
        409: {"model": ErrorResponse, "description": "Garment name already exists"},
    }
)
async def create_garment(
    payload: NewGarment,
    garment_service: Annotated[GarmentServiceInterface, Depends(get_garment_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> GarmentOut:
    return await garment_service.create(user_id=current_user.id, new_garment=payload)


@router.patch(
    "/{id}",
    response_model=GarmentOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Garment or referenced entity not found"},
        409: {"model": ErrorResponse, "description": "Garment name already exists"},
    }
)
async def update_garment(
    id: int,
    payload: UpdateGarment,
    garment_service: Annotated[GarmentServiceInterface, Depends(get_garment_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> GarmentOut:
    return await garment_service.update(user_id=current_user.id, id=id, update_data=payload)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Garment not found"},
    }
)
async def delete_garment(
    id: int,
    garment_service: Annotated[GarmentServiceInterface, Depends(get_garment_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> None:
    await garment_service.delete(user_id=current_user.id, id=id)


@router.post(
    "/{id}/images",
    response_model=GarmentImageOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid image or corrupted"},
        404: {"model": ErrorResponse, "description": "Garment not found"},
        413: {"model": ErrorResponse, "description": "Image file too large"},
        415: {"model": ErrorResponse, "description": "Unsupported image format"},
    },
)
async def upload_garment_image(
    id: int,
    file: Annotated[UploadFile, File(description="Image file (JPEG, PNG, WebP)")],
    garment_service: Annotated[GarmentServiceInterface, Depends(get_garment_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    is_primary: Annotated[bool, Form(description="Whether this is the primary image")] = False,
    order: Annotated[int, Form(description="Display order")] = 0,
) -> GarmentImageOut:
    return await garment_service.add_image(
        user_id=current_user.id,
        garment_id=id,
        file=file,
        is_primary=is_primary,
        order=order,
    )


@router.post(
    "/{id}/images/batch",
    response_model=list[GarmentImageOut],
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid image or corrupted"},
        404: {"model": ErrorResponse, "description": "Garment not found"},
        413: {"model": ErrorResponse, "description": "Image file too large"},
        415: {"model": ErrorResponse, "description": "Unsupported image format"},
    },
)
async def upload_garment_images_batch(
    id: int,
    files: Annotated[list[UploadFile], File(description="List of image files (JPEG, PNG, WebP)")],
    garment_service: Annotated[GarmentServiceInterface, Depends(get_garment_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[GarmentImageOut]:
    return await garment_service.add_images_batch(
        user_id=current_user.id,
        garment_id=id,
        files=files,
    )


@router.delete(
    "/{id}/images/batch",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Garment or image not found"},
    },
)
async def delete_garment_images_batch(
    id: int,
    body: BatchDeleteImagesRequest,
    garment_service: Annotated[GarmentServiceInterface, Depends(get_garment_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    await garment_service.delete_images_batch(
        user_id=current_user.id,
        garment_id=id,
        image_ids=body.image_ids,
    )


@router.delete(
    "/{id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Garment or image not found"},
    },
)
async def delete_garment_image(
    id: int,
    image_id: int,
    garment_service: Annotated[GarmentServiceInterface, Depends(get_garment_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    await garment_service.delete_image(
        user_id=current_user.id,
        garment_id=id,
        image_id=image_id,
    )

