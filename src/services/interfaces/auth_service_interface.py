from abc import ABC, abstractmethod

from schemas.auth import UserRegister, UserRegisterOut, UserLogin, UserLoginOut, AccountVerification

class AuthServiceInterface(ABC):
    @abstractmethod
    async def register_user(self, new_user: UserRegister) -> UserRegisterOut: ...

    @abstractmethod
    async def local_login(self, user_credentials: UserLogin) -> tuple[UserLoginOut, str]: ...

    @abstractmethod
    async def refresh_tokens(self, refresh_token: str | None) -> tuple[UserLoginOut, str]: ... 

    @abstractmethod
    async def logout(self, refresh_token: str | None) -> None: ...

    @abstractmethod
    async def forgot_password(self, user_email: str) -> str | None: ...

    @abstractmethod
    async def reset_password(self, reset_token: str, new_password: str) -> None: ...

    @abstractmethod
    async def get_verification_code(self, email: str) -> str | None: ...

    @abstractmethod
    async def verify_user(self, user_verification_data: AccountVerification) -> None: ...