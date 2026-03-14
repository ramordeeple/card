import asyncio
import sys
from os.path import abspath, dirname
from sqlalchemy import pool
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from src.core.config import settings
from src.db.session import Base
from src.db.models.user import User
from src.db.models.card import Card

target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online():
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_online()

else:
    run_migrations_online()