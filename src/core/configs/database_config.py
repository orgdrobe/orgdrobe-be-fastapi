from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseConfig(BaseSettings):
    DIALECT_DRIVER: str
    USERNAME: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME_OR_PATH: str
    SHOW_LOGGING: bool = False

    model_config = SettingsConfigDict(
        env_prefix="DB_", 
        extra="ignore",
        env_file=(".env", "../.env"),
        env_file_encoding='utf-8',
    )

database_config = DatabaseConfig() # type: ignore[call-arg]