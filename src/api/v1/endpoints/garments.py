from typing import Annotated
from fastapi import APIRouter, Depends, status

from schemas.garment import NewGarment, GarmentOut, UpdateGarment
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
