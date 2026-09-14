from typing import Annotated
from fastapi import APIRouter, Depends, status

from schemas.usage import NewUsage, UsageOut, UpdateUsage
from services.interfaces import UsageServiceInterface
from schemas.errors import ErrorResponse
from dependencies import get_usage_service, get_current_user, require_role
from models import User

router = APIRouter()


@router.get(
    "/", 
    response_model=list[UsageOut],
    status_code=status.HTTP_200_OK
)
async def uses_all(
    usage_service: Annotated[UsageServiceInterface, Depends(get_usage_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100
) -> list[UsageOut]:
    return await usage_service.get_all(skip=skip, limit=limit)


@router.get(
    "/{id}", 
    response_model=UsageOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Usage not found"},
    }
)
async def usage_by_id(
    id: int, 
    usage_service: Annotated[UsageServiceInterface, Depends(get_usage_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> UsageOut:
    result = await usage_service.get_by_id(id)
    return result


@router.post(
    "/",
    response_model=UsageOut,
    status_code=status.HTTP_201_CREATED
)
async def create_usage(
    payload: NewUsage,
    usage_service: Annotated[UsageServiceInterface, Depends(get_usage_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> UsageOut:
    return await usage_service.create(payload)


@router.patch(
    "/{id}",
    response_model=UsageOut,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Usage not found"},
    }
)
async def update_usage(
    id: int,
    payload: UpdateUsage,
    usage_service: Annotated[UsageServiceInterface, Depends(get_usage_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> UsageOut:
    return await usage_service.update(id, payload)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Usage not found"},
    }
)
async def delete_usage(
    id: int,
    usage_service: Annotated[UsageServiceInterface, Depends(get_usage_service)],
    current_user: Annotated[User, Depends(require_role(["admin"]))]
) -> None:
    await usage_service.delete(id)
