from fastapi_mail import ConnectionConfig

from services import EmailService
from services.interfaces import EmailServiceInterface
from core.configs import email_config

def get_email_service() -> EmailServiceInterface:
        connection_config = ConnectionConfig(
        MAIL_USERNAME=email_config.USERNAME,
        MAIL_PASSWORD=email_config.PASSWORD,
        MAIL_FROM=email_config.FROM,
        MAIL_PORT=email_config.PORT,
        MAIL_SERVER=email_config.SERVER,
        MAIL_FROM_NAME=email_config.FROM_NAME,
        MAIL_STARTTLS=False,         # Port 465 uses implicit SSL, not STARTTLS
        MAIL_SSL_TLS=True,           # This is required for Port 465
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
        )

        return EmailService(connection_config)