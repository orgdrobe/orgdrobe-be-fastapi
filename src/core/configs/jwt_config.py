from pydantic_settings import BaseSettings, SettingsConfigDict

class JwtConfig(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    RESET_EMAIL_TOKEN_EXPIRE_MINUTES: int = 15

    model_config = SettingsConfigDict(
        env_prefix="SECURITY_", 
        extra="ignore",
        env_file=(".env"),
        env_file_encoding='utf-8'
    )

jwt_config = JwtConfig() # type: ignore[call-arg]