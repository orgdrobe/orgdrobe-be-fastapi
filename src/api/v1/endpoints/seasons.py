from typing import Annotated
from fastapi import APIRouter, Depends, status

from schemas.season import NewSeason, SeasonOut, UpdateSeason
from services.interfaces import SeasonServiceInterface
from schemas.errors import ErrorResponse
from dependencies import get_season_service, get_current_user, require_role
from models import User

router = APIRouter()


@router.get(
    "/", 
    response_model=list[SeasonOut],
    status_code=status.HTTP_200_OK
)
async def seasons_all(
    season_service: Annotated[SeasonServiceInterface, Depends(get_season_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100
) -> list[SeasonOut]:
    return await season_service.get_all(skip=skip, limit=limit)


@router.get(
    "/{id}", 
    response_model=SeasonOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Season not found"},
    }
)
async def season_by_id(
    id: int, 
    season_service: Annotated[SeasonServiceInterface, Depends(get_season_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> SeasonOut:
    result = await season_service.get_by_id(id)
    return result


@router.post(
    "/",
    response_model=SeasonOut,
    status_code=status.HTTP_201_CREATED
)
async def create_season(
    payload: NewSeason,
    season_service: Annotated[SeasonServiceInterface, Depends(get_season_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> SeasonOut:
    return await season_service.create(payload)


@router.patch(
    "/{id}",
    response_model=SeasonOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Season not found"},
    }
)
async def update_season(
    id: int,
    payload: UpdateSeason,
    season_service: Annotated[SeasonServiceInterface, Depends(get_season_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> SeasonOut:
    return await season_service.update(id, payload)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Season not found"},
    }
)
async def delete_season(
    id: int,
    season_service: Annotated[SeasonServiceInterface, Depends(get_season_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> None:
    await season_service.delete(id)
