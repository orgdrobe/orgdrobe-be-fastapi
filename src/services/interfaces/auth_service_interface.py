from abc import ABC, abstractmethod

from schemas.auth import (
    AccountVerification,
    UserLogin,
    UserLoginOut,
    UserRegister,
    UserRegisterOut,
)


class AuthServiceInterface(ABC):
    """Interface for authentication, authorization, and user account lifecycle."""

    @abstractmethod
    async def register_user(self, new_user: UserRegister) -> UserRegisterOut:
        """Register a new user account with hashed password and initial role."""
        ...

    @abstractmethod
    async def local_login(self, user_credentials: UserLogin) -> tuple[UserLoginOut, str]:
        """Authenticate user credentials, returning user info and tokens."""
        ...

    @abstractmethod
    async def refresh_tokens(self, refresh_token: str | None) -> tuple[UserLoginOut, str]:
        """Validate existing refresh token and issue a new token pair."""
        ...

    @abstractmethod
    async def logout(self, refresh_token: str | None) -> None:
        """Revoke active refresh token and invalidate the user session."""
        ...

    @abstractmethod
    async def forgot_password(self, user_email: str) -> str | None:
        """Generate a secure password reset token for the specified email."""
        ...

    @abstractmethod
    async def reset_password(self, reset_token: str, new_password: str) -> None:
        """Update user password using a validated password reset token."""
        ...

    @abstractmethod
    async def get_verification_code(self, email: str) -> str | None:
        """Generate or retrieve a one-time email account verification code."""
        ...

    @abstractmethod
    async def verify_user(self, user_verification_data: AccountVerification) -> None:
        """Verify user account ownership using the submitted verification code."""
        ...