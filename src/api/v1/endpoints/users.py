from typing import Annotated
from fastapi import APIRouter, Depends, File, UploadFile, status

from dependencies import get_current_user, get_user_service
from models import User
from schemas.errors import ErrorResponse
from schemas.user import UserAvatarOut
from services.interfaces import UserServiceInterface

router = APIRouter()


@router.get("/test")
def test_route() -> dict[str, str]:
    return {"message": "Hello world!"}


@router.post(
    "/me/avatar",
    response_model=UserAvatarOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid image or corrupted"},
        413: {"model": ErrorResponse, "description": "Image file too large"},
        415: {"model": ErrorResponse, "description": "Unsupported image format"},
    },
)
async def upload_my_avatar(
    file: Annotated[UploadFile, File(description="Avatar image file (JPEG, PNG, WebP)")],
    user_service: Annotated[UserServiceInterface, Depends(get_user_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserAvatarOut:
    return await user_service.upload_avatar(
        user_id=current_user.id,
        file=file,
    )


@router.get(
    "/me/avatar",
    response_model=UserAvatarOut | None,
    status_code=status.HTTP_200_OK,
)
async def get_my_avatar(
    user_service: Annotated[UserServiceInterface, Depends(get_user_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserAvatarOut | None:
    return await user_service.get_avatar(user_id=current_user.id)


@router.delete(
    "/me/avatar",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Avatar not found"},
    },
)
async def delete_my_avatar(
    user_service: Annotated[UserServiceInterface, Depends(get_user_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    await user_service.delete_avatar(user_id=current_user.id)