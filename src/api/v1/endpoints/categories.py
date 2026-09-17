from fastapi import APIRouter

from typing import Annotated
from fastapi import APIRouter, Depends, status

from schemas.master_category import NewMasterCategory, MasterCategoryOut, UpdateMasterCategory
from schemas.sub_category import NewSubCategory, SubCategoryOut, UpdateSubCategory
from services.interfaces import MasterCategoryServiceInterface, SubCategoryServiceInterface
from schemas.errors import ErrorResponse
from dependencies import get_master_category_service, get_sub_category_service, get_current_user, require_role
from models import User

router = APIRouter()


@router.get(
    "/master/", 
    response_model=list[MasterCategoryOut],
    status_code=status.HTTP_200_OK
)
async def master_categories_all(
    category_service: Annotated[MasterCategoryServiceInterface, Depends(get_master_category_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100
) -> list[MasterCategoryOut]:
    return await category_service.get_all(skip=skip, limit=limit)


@router.get(
    "/master/{id}", 
    response_model=MasterCategoryOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Master category not found"},
    }
)
async def master_category_by_id(
    id: int, 
    category_service: Annotated[MasterCategoryServiceInterface, Depends(get_master_category_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> MasterCategoryOut:
    result = await category_service.get_by_id(id)
    return result


@router.post(
    "/master/",
    response_model=MasterCategoryOut,
    status_code=status.HTTP_201_CREATED
)
async def create_master_category(
    payload: NewMasterCategory,
    category_service: Annotated[MasterCategoryServiceInterface, Depends(get_master_category_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> MasterCategoryOut:
    return await category_service.create(payload)


@router.patch(
    "/master/{id}",
    response_model=MasterCategoryOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Master category not found"},
    }
)
async def update_master_category(
    id: int,
    payload: UpdateMasterCategory,
    category_service: Annotated[MasterCategoryServiceInterface, Depends(get_master_category_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> MasterCategoryOut:
    return await category_service.update(id, payload)


@router.delete(
    "/master/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Master category not found"},
    }
)
async def delete_master_category(
    id: int,
    category_service: Annotated[MasterCategoryServiceInterface, Depends(get_master_category_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> None:
    await category_service.delete(id)


# ---------------------------------------------------------
# SUB CATEGORIES
# ---------------------------------------------------------

@router.get(
    "/sub/", 
    response_model=list[SubCategoryOut],
    status_code=status.HTTP_200_OK
)
async def sub_categories_all(
    category_service: Annotated[SubCategoryServiceInterface, Depends(get_sub_category_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100
) -> list[SubCategoryOut]:
    return await category_service.get_all(skip=skip, limit=limit)


@router.get(
    "/sub/{id}", 
    response_model=SubCategoryOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Sub category not found"},
    }
)
async def sub_category_by_id(
    id: int, 
    category_service: Annotated[SubCategoryServiceInterface, Depends(get_sub_category_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> SubCategoryOut:
    result = await category_service.get_by_id(id)
    return result


@router.post(
    "/sub/",
    response_model=SubCategoryOut,
    status_code=status.HTTP_201_CREATED
)
async def create_sub_category(
    payload: NewSubCategory,
    category_service: Annotated[SubCategoryServiceInterface, Depends(get_sub_category_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> SubCategoryOut:
    return await category_service.create(payload)


@router.patch(
    "/sub/{id}",
    response_model=SubCategoryOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Sub category not found"},
    }
)
async def update_sub_category(
    id: int,
    payload: UpdateSubCategory,
    category_service: Annotated[SubCategoryServiceInterface, Depends(get_sub_category_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> SubCategoryOut:
    return await category_service.update(id, payload)


@router.delete(
    "/sub/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Sub category not found"},
    }
)
async def delete_sub_category(
    id: int,
    category_service: Annotated[SubCategoryServiceInterface, Depends(get_sub_category_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> None:
    await category_service.delete(id)
