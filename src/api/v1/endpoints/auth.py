from typing import Annotated

from fastapi import APIRouter, Response, BackgroundTasks, Depends, Cookie
from fastapi.security import OAuth2PasswordRequestForm

from core.configs import jwt_config
from schemas.errors import ErrorResponse
from schemas.auth import (
    UserRegister, UserRegisterOut, UserLogin, UserLoginOut, 
    SendVerificationCode, AccountVerification, ForgotPassword,
    ResetPassword)
from dependencies import get_auth_service, get_email_service, get_current_user, require_role
from services.interfaces import AuthServiceInterface, EmailServiceInterface
from models import User

router = APIRouter()

@router.post(
    "/register", 
    response_model=UserRegisterOut,
    status_code=201,
    responses={
        409: {"model": ErrorResponse, "description": "Username or email already exist"},
        404: {"model": ErrorResponse, "description": "User role not found"},
    }
)
async def register(
    payload: UserRegister, 
    auth_service: Annotated[AuthServiceInterface, Depends(get_auth_service)],
    email_service: Annotated[EmailServiceInterface, Depends(get_email_service)],
    background: BackgroundTasks
) -> UserRegisterOut:
    result = await auth_service.register_user(payload)
    code = await auth_service.get_verification_code(result.email)
    if code is not None:
        background.add_task(email_service.send_verification_email, result.email, code)
    return result



@router.post(
    "/login", 
    response_model=UserLoginOut,
    status_code=200,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid username or password."},
        403: {"model": ErrorResponse, "description": "Email not verified."}
    }
)
async def local_login(
    response: Response, 
    payload: Annotated[OAuth2PasswordRequestForm, Depends()], 
    auth_service: Annotated[AuthServiceInterface, Depends(get_auth_service)]
) -> UserLoginOut:
    login_result, refresh_token  = await auth_service.local_login(UserLogin(email=payload.username, password=payload.password))
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True, # Dev = False
        samesite="lax", 
        max_age=jwt_config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )
    return login_result


@router.post(
        "/refresh",
        response_model = UserLoginOut,
        status_code = 200,
        responses = {
                 401: {"model": ErrorResponse, "description": "Authentication errors during token refresh"}
        }
)
async def refresh_tokens(
    response: Response, 
    auth_service: Annotated[AuthServiceInterface, Depends(get_auth_service)],
    refresh_token: Annotated[str | None, Cookie()] = None
) -> UserLoginOut:
    login_result, new_refresh_token = await auth_service.refresh_tokens(refresh_token)
    print(new_refresh_token)
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True, # Dev = False
        samesite="lax", 
        max_age=jwt_config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )
    return login_result


@router.post(
        "/logout",
        status_code = 204,
        responses = {}
)
async def logout(
    response: Response, 
    auth_service: Annotated[AuthServiceInterface, Depends(get_auth_service)],
    refresh_token: Annotated[str | None, Cookie()] = None
) -> Response:
    await auth_service.logout(refresh_token)
    response = Response(status_code=204)
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        samesite="lax")
    return response


# ATTENTION: Only available for the local provider.
@router.post(
        "/forgot-password",
        status_code = 204,
        responses = {}
)
async def forgot_password(
    response: Response, 
    payload: ForgotPassword,
    auth_service: Annotated[AuthServiceInterface, Depends(get_auth_service)],
    email_service: Annotated[EmailServiceInterface, Depends(get_email_service)],
    background: BackgroundTasks
) -> Response:
    reset_token = await auth_service.forgot_password(payload.email)
    if reset_token is not None:
        background.add_task(email_service.send_forgot_password_email, payload.email, reset_token)
    response = Response(status_code=204)
    return response


# ATTENTION: Only available for the local provider.
@router.post(
        "/reset-password",
        status_code = 204,
        responses = {
             401: {"model": ErrorResponse, "description": "Reset token is invalid or erxpired"},
        }
)
async def reset_password(
    response: Response, 
    payload: ResetPassword,
    auth_service: Annotated[AuthServiceInterface, Depends(get_auth_service)]
) -> Response:
    await auth_service.reset_password(payload.token, payload.password)
    response = Response(status_code=204)
    return response


@router.post(
        "/activation-code",
        status_code = 204,
        responses = {
            429: {"model": ErrorResponse, "description": "Attempt limit exceeded"}
        }
)
async def send_verification_code(
    response: Response,
    payload: SendVerificationCode,
    auth_service: Annotated[AuthServiceInterface, Depends(get_auth_service)],
    email_service: Annotated[EmailServiceInterface, Depends(get_email_service)],
    background: BackgroundTasks
) -> Response:
    code = await auth_service.get_verification_code(payload.email)
    if code is not None:
        background.add_task(email_service.send_verification_email, payload.email, code)
    response = Response(status_code=204)
    return response


@router.post(
        "/verification",
        status_code = 204,
        responses = {
            400: {"model": ErrorResponse, "description" : "Invalid email or verification code, or the verification code has expired."}
        }
)
async def verify_user(
    response: Response,
    payload: AccountVerification,
    auth_service: Annotated[AuthServiceInterface, Depends(get_auth_service)]
) -> Response:
    await auth_service.verify_user(payload)
    response = Response(status_code=204)
    return response





# TEST ROUTE
@router.get("/me", response_model=dict)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return {"message": f"{current_user.username}"}

@router.get("/admin", response_model=dict)
async def read_role_user(
    current_user: User = Depends(require_role(["admin"]))
):
    return {"message": f"you are user!"}

#class TransactionContext()
#   def rollback()
#   def commit()

# @router.post("/login", response_model=TempData)
# async def login(db: TempData, credentials: TempData):
#     return None

# @router.post("/google", response_model=TempData)
# async def google(db: TempData, credentials: TempData):
#     return None