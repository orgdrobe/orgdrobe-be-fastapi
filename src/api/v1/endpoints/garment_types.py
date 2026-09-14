from typing import Annotated
from fastapi import APIRouter, Depends, status

from schemas.garment_type import NewGarmentType, GarmentTypeOut, UpdateGarmentType
from services.interfaces import GarmentTypeServiceInterface
from schemas.errors import ErrorResponse
from dependencies import get_garment_type_service, get_current_user, require_role
from models import User

router = APIRouter()


@router.get(
    "/", 
    response_model=list[GarmentTypeOut],
    status_code=status.HTTP_200_OK
)
async def garment_types_all(
    garment_type_service: Annotated[GarmentTypeServiceInterface, Depends(get_garment_type_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100
) -> list[GarmentTypeOut]:
    return await garment_type_service.get_all(skip=skip, limit=limit)


@router.get(
    "/{id}", 
    response_model=GarmentTypeOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Garment type not found"},
    }
)
async def garment_type_by_id(
    id: int, 
    garment_type_service: Annotated[GarmentTypeServiceInterface, Depends(get_garment_type_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> GarmentTypeOut:
    result = await garment_type_service.get_by_id(id)
    return result


@router.post(
    "/",
    response_model=GarmentTypeOut,
    status_code=status.HTTP_201_CREATED
)
async def create_garment_type(
    payload: NewGarmentType,
    garment_type_service: Annotated[GarmentTypeServiceInterface, Depends(get_garment_type_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> GarmentTypeOut:
    return await garment_type_service.create(payload)


@router.patch(
    "/{id}",
    response_model=GarmentTypeOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Garment type not found"},
    }
)
async def update_garment_type(
    id: int,
    payload: UpdateGarmentType,
    garment_type_service: Annotated[GarmentTypeServiceInterface, Depends(get_garment_type_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> GarmentTypeOut:
    return await garment_type_service.update(id, payload)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Garment type not found"},
    }
)
async def delete_garment_type(
    id: int,
    garment_type_service: Annotated[GarmentTypeServiceInterface, Depends(get_garment_type_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> None:
    await garment_type_service.delete(id)