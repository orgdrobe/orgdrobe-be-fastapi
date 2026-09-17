from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.configs import database_config

def build_database_uri() -> str:
    return f"{database_config.DIALECT_DRIVER}://{database_config.USERNAME}:{database_config.PASSWORD}@{database_config.HOST}:{database_config.PORT}/{database_config.NAME_OR_PATH}"

CONNECTION_STRING = build_database_uri()
print(CONNECTION_STRING)

engine = create_async_engine(CONNECTION_STRING, echo=database_config.SHOW_LOGGING)

async_session_factory = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)