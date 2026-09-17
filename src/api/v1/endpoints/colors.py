from typing import Annotated
from fastapi import APIRouter, Depends, status

from schemas.color import NewColor, ColorOut, UpdateColor
from services.interfaces import ColorServiceInterface
from schemas.errors import ErrorResponse
from dependencies import get_color_service, get_current_user, require_role
from models import User

router = APIRouter()


@router.get(
    "/", 
    response_model=list[ColorOut],
    status_code=status.HTTP_200_OK
)
async def colors_all(
    color_service: Annotated[ColorServiceInterface, Depends(get_color_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100
) -> list[ColorOut]:
    return await color_service.get_all(skip=skip, limit=limit)


@router.get(
    "/{id}", 
    response_model=ColorOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Color not found"},
    }
)
async def color_by_id(
    id: int, 
    color_service: Annotated[ColorServiceInterface, Depends(get_color_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> ColorOut:
    result = await color_service.get_by_id(id)
    return result


@router.post(
    "/",
    response_model=ColorOut,
    status_code=status.HTTP_201_CREATED
)
async def create_color(
    payload: NewColor,
    color_service: Annotated[ColorServiceInterface, Depends(get_color_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> ColorOut:
    return await color_service.create(payload)


@router.patch(
    "/{id}",
    response_model=ColorOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Color not found"},
    }
)
async def update_color(
    id: int,
    payload: UpdateColor,
    color_service: Annotated[ColorServiceInterface, Depends(get_color_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> ColorOut:
    return await color_service.update(id, payload)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Color not found"},
    }
)
async def delete_color(
    id: int,
    color_service: Annotated[ColorServiceInterface, Depends(get_color_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> None:
    await color_service.delete(id)