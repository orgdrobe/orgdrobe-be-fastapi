from abc import ABC, abstractmethod


class EmailServiceInterface(ABC):
    """Interface for sending transactional emails (verification, password reset, notifications)."""

    @abstractmethod
    async def send_verification_email(self, user_email: str, code: str) -> None:
        """Send an email verification code to the specified user address."""
        ...

    @abstractmethod
    async def send_forgot_password_email(self, user_email: str, reset_token: str) -> None:
        """Send a password recovery email containing the password reset link or token."""
        ...