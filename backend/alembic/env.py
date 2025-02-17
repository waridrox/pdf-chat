import asyncio
from alembic import context
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine
from app.db import Base, engine, get_database_url, create_engine_with_retry


config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata


async def run_migrations_online():
    """Run migrations in 'online' mode with async support."""
    connectable = create_engine_with_retry(get_database_url())

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


asyncio.run(run_migrations_online())


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""

    url = get_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
