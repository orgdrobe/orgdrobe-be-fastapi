from abc import ABC, abstractmethod


class EmailServiceInterface(ABC):
    @abstractmethod
    async def send_verification_email(self, user_email: str, code: str) -> None: ...

    @abstractmethod
    async def send_forgot_password_email(self, user_email: str, reset_token: str) -> None: ...