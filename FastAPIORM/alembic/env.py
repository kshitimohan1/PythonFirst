from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.model import Base
from app.config import settings
from urllib.parse import quote_plus
from configparser import RawConfigParser

config = context.config

# Use RawConfigParser to avoid % interpolation issue
raw_config = RawConfigParser()
raw_config.read(config.config_file_name)
config.file_config = raw_config

password = quote_plus(settings.database_password)

config.set_main_option(
    "sqlalchemy.url",
    f"postgresql+psycopg2://{settings.database_username}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
