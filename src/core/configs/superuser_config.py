from pydantic_settings import BaseSettings, SettingsConfigDict

class SuperUserConfig(BaseSettings):
    SUPERUSER_USERNAME: str
    SUPERUSER_EMAIL: str
    SUPERUSER_PASSWORD: str
    
    model_config = SettingsConfigDict(
        env_prefix="FIRST_", 
        extra="ignore",
        env_file=(".env", "../.env"),
        env_file_encoding='utf-8',
    )

superuser_config = SuperUserConfig() # type: ignore[call-arg]