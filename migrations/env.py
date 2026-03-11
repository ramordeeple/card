import sys
from os.path import abspath, dirname
from sqlalchemy import engine_from_config, pool
from alembic import context

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from src.core.config import settings
from src.db.session import Base
from src.db.models.user import User
from src.db.models.card import Card

target_metadata = Base.metadata

def run_migrations_online():
    conf = context.config.get_section(context.config.config_ini_section)
    conf["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = engine_from_config(
        conf,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()