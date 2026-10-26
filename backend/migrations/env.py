"""Alembic migrations, SQLite local or PostgreSQL using DATABASE_URL."""
from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine, pool
from backend.app.config import database_url
from backend.app.db import Base

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)
target_metadata = Base.metadata

def offline():
    context.configure(url=database_url(), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def online():
    engine = create_engine(database_url(), poolclass=pool.NullPool)
    with engine.connect() as conn:
        context.configure(connection=conn, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()

if context.is_offline_mode():
    offline()
else:
    online()
