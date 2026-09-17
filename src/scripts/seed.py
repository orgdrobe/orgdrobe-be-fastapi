import asyncio
import functools

import typer 
import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security.crypto import pwd_context
from core.configs.superuser_config import superuser_config
from core.configs.logging_config import configure_logging
from core.enums.auth_roles import AuthRole
from core.enums.auth_providers import AuthProvider
from core.database.database_context import async_session_factory
from models import Role, User, UserIdentity, UserRole


cli = typer.Typer()

configure_logging()
structlog.contextvars.clear_contextvars()
structlog.contextvars.bind_contextvars(
    process_type="cli_script",
    script_name="db_seed"
)

logger = structlog.get_logger(__name__)

def db_session(async_session_factory):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with async_session_factory() as session:
                try:
                    result = await func(session, *args, **kwargs)
                    await session.commit()
                    logger.info(f"{func.__name__} completed successfully")
                    return result
                except Exception as e:
                    await session.rollback()
                    logger.exception(f"{func.__name__} failed", exc_info=e)
                    raise
        return wrapper
    return decorator


async def create_or_get_roles(session: AsyncSession) -> list[Role]:
    roles_to_seed = [AuthRole.Admin, AuthRole.User]
    roles_description = ["Administrator", "Common user"]

    resulting_roles = [] 
    
    for index, role_name in enumerate(roles_to_seed):
        log = logger.bind(role_name=role_name)
        
        stmt = select(Role).where(Role.name == role_name)
        result = await session.execute(stmt)
        existing_role = result.scalar_one_or_none()
        
        if existing_role is None:
            new_role = Role(name=role_name, description=roles_description[index])
            session.add(new_role)
            await session.flush()
            await session.refresh(new_role)
            resulting_roles.append(new_role)
            
            log.info("role_added", status="created")
        else:
            resulting_roles.append(existing_role)
            log.info("role_already_exists", status="skipped")
            
    return resulting_roles

async def create_or_get_first_superuser(session: AsyncSession) -> User:
    username = superuser_config.SUPERUSER_USERNAME
    email = superuser_config.SUPERUSER_EMAIL
    password = superuser_config.SUPERUSER_PASSWORD


    log = logger.bind(user_email=email)

    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        log.info("creating_first_superuser")
        
        user = User(
            username=username,
            email=email,
            is_email_verified=True
        )
        session.add(user)
        await session.flush()
        await session.refresh(user)

        password_hash = pwd_context.hash(password)
        user_identity = UserIdentity( 
            user_id=user.id,
            provider=AuthProvider.local,
            provider_id=user.email,
            password_hash=password_hash
        )
        session.add(user_identity) 

        roles = await create_or_get_roles(session)

        if roles:
            for role in roles:
                user_role = UserRole(
                    user_id=user.id,
                    role_id=role.id
                )
                session.add(user_role)

        log.info("superuser_created_successfully", status="success")
        return user
    else:
        log.info("superuser_already_exists", status="skipped")
        return user

        


@db_session(async_session_factory)
async def seeding_all(session: AsyncSession) -> None:
    logger.info("starting_seeding_process")
    await create_or_get_roles(session)
    await create_or_get_first_superuser(session)
            
@db_session(async_session_factory)
async def seeding_roles(session: AsyncSession) -> None:
    logger.info("starting_seeding_process")
    await create_or_get_roles(session)

@db_session(async_session_factory)
async def seeding_first_superuser(session: AsyncSession) -> None:
    logger.info("starting_seeding_process")
    await create_or_get_first_superuser(session)


@cli.command(name="all")
def seed_all() -> None:
    """
    Запускає процес наповнення бази даних ВСІМА початковими даними.
    """
    asyncio.run(seeding_all())

@cli.command(name="roles")
def seed_all_roles() -> None:
    """
    Запускає процес наповнення бази даних ТІЛЬКИ ролями.
    """
    asyncio.run(seeding_roles())

@cli.command(name="superuser")
def seed_first_superuser() -> None:
    """
    Запускає процес наповнення бази даних ТІЛЬКИ суперкористувачем та ролями.
    """
    asyncio.run(seeding_first_superuser())


if __name__ == "__main__":
    cli()