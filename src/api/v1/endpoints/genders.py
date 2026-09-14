from typing import Annotated
from fastapi import APIRouter, Depends, status

from schemas.gender import NewGender, GenderOut, UpdateGender
from services.interfaces import GenderServiceInterface
from schemas.errors import ErrorResponse
from dependencies import get_gender_service, get_current_user, require_role
from models import User

router = APIRouter()


@router.get(
    "/", 
    response_model=list[GenderOut],
    status_code=status.HTTP_200_OK
)
async def genders_all(
    gender_service: Annotated[GenderServiceInterface, Depends(get_gender_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100
) -> list[GenderOut]:
    return await gender_service.get_all(skip=skip, limit=limit)


@router.get(
    "/{id}", 
    response_model=GenderOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Gender not found"},
    }
)
async def gender_by_id(
    id: int, 
    gender_service: Annotated[GenderServiceInterface, Depends(get_gender_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> GenderOut:
    result = await gender_service.get_by_id(id)
    return result


@router.post(
    "/",
    response_model=GenderOut,
    status_code=status.HTTP_201_CREATED
)
async def create_gender(
    payload: NewGender,
    gender_service: Annotated[GenderServiceInterface, Depends(get_gender_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> GenderOut:
    return await gender_service.create(payload)


@router.patch(
    "/{id}",
    response_model=GenderOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Gender not found"},
    }
)
async def update_gender(
    id: int,
    payload: UpdateGender,
    gender_service: Annotated[GenderServiceInterface, Depends(get_gender_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> GenderOut:
    return await gender_service.update(id, payload)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Gender not found"},
    }
)
async def delete_gender(
    id: int,
    gender_service: Annotated[GenderServiceInterface, Depends(get_gender_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> None:
    await gender_service.delete(id)