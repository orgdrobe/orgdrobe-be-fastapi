from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class EmailConfig(BaseSettings):
    USERNAME: str
    PASSWORD: SecretStr
    FROM: str
    PORT: int
    SERVER: str
    FROM_NAME: str

    model_config = SettingsConfigDict(
        env_prefix="MAIL_", 
        extra="ignore",
        env_file=(".env"),
        env_file_encoding='utf-8'
    )

email_config = EmailConfig() # type: ignore[call-arg]