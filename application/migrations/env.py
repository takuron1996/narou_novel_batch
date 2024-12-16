from importlib import import_module
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

from config.env import postgre_settings
from models.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

config.set_section_option(
    "alembic", "POSTGRES_USER", postgre_settings.POSTGRES_USER
)
config.set_section_option(
    "alembic", "POSTGRES_PASSWORD", postgre_settings.POSTGRES_PASSWORD
)
config.set_section_option(
    "alembic", "POSTGRES_DB", postgre_settings.POSTGRES_DB
)
config.set_section_option(
    "alembic", "POSTGRES_NAME", postgre_settings.POSTGRES_NAME
)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


def import_migration_module(module):
    """マイグレーションに含めたいモジュールをimport."""
    for file_name in (p.name for p in Path(module).iterdir() if p.is_file()):
        if file_name in {"__init__.py", "base.py"}:
            continue
        file_name = file_name.replace(".py", "")
        import_module(f"{module}.{file_name}")


# データモデルを記述しているディレクトリ名を指定
import_migration_module("models")
# 最初から書いてあるtarget_metadataに生成したBaseのmetadataを設定
target_metadata = Base.metadata

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
