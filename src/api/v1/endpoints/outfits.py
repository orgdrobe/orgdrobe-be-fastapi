from typing import Annotated
from fastapi import APIRouter, Depends, status

from schemas.outfit import NewOutfit, OutfitOut, UpdateOutfit
from services.interfaces import OutfitServiceInterface
from schemas.errors import ErrorResponse
from dependencies import get_outfit_service, get_current_user
from models import User

router = APIRouter()


@router.get(
    "/",
    response_model=list[OutfitOut],
    status_code=status.HTTP_200_OK,
)
async def outfits_all_by_user(
    outfit_service: Annotated[OutfitServiceInterface, Depends(get_outfit_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100
) -> list[OutfitOut]:
    return await outfit_service.get_all_by_user_id(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )


@router.get(
    "/{id}",
    response_model=OutfitOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Outfit not found"},
    }
)
async def outfit_by_id(
    id: int,
    outfit_service: Annotated[OutfitServiceInterface, Depends(get_outfit_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> OutfitOut:
    return await outfit_service.get_by_id(user_id=current_user.id, id=id)


@router.post(
    "/",
    response_model=OutfitOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"model": ErrorResponse, "description": "Garment not found"},
        409: {"model": ErrorResponse, "description": "Outfit name already exists"},
    }
)
async def create_outfit(
    payload: NewOutfit,
    outfit_service: Annotated[OutfitServiceInterface, Depends(get_outfit_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> OutfitOut:
    return await outfit_service.create(user_id=current_user.id, new_outfit=payload)


@router.patch(
    "/{id}",
    response_model=OutfitOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Outfit or Garment not found"},
        409: {"model": ErrorResponse, "description": "Outfit name already exists"},
    }
)
async def update_outfit(
    id: int,
    payload: UpdateOutfit,
    outfit_service: Annotated[OutfitServiceInterface, Depends(get_outfit_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> OutfitOut:
    return await outfit_service.update(user_id=current_user.id, id=id, update_data=payload)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Outfit not found"},
    }
)
async def delete_outfit(
    id: int,
    outfit_service: Annotated[OutfitServiceInterface, Depends(get_outfit_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> None:
    await outfit_service.delete(user_id=current_user.id, id=id)


# --- Outfit Garments (Non-CRUD - currently commented out) ---
# @router.get("/{id}/garments", response_model=list[TempData])
# async def get_outfit_garments(id: int, db: TempData, current_user: TempData):
#     return None
#
# @router.get("/{id}/garments/unused", response_model=list[TempData])
# async def get_outfit_garments_unused(id: int, db: TempData, current_user: TempData):
#     return None
#
# @router.put("/{id}/garments")
# async def update_outfit_garments_by_ids(id: int, garments_update: TempData, db: TempData, current_user: TempData):
#     return None
#
# @router.post("/{outfit_id}/garments/{garment_id}")
# async def add_garment_to_outfit(outfit_id: int, garment_id: int, db: TempData, current_user: TempData):
#     return None
#
# @router.delete("/{outfit_id}/garments/{garment_id}")
# async def delete_garment_from_outfit(outfit_id: int, garment_id: int, db: TempData, current_user: TempData):
#     return None


# --- Outfit Generation (Non-CRUD - currently commented out) ---
# @router.post("/generate/random/garments", response_model=list[TempData])
# async def create_random_garments_for_outfit(params: TempData, db: TempData, current_user: TempData):
#     return None
#
# @router.post("/generate/autocomplete/garments", response_model=list[TempData])
# async def generate_autocomplete_garments(params: TempData, db: TempData, current_user: TempData):
#     return None

