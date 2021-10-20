import os

import pytest

os.environ['TESTING'] = 'True'

from alembic import command
from alembic.config import Config
from sqlalchemy_utils import create_database, drop_database

from app.core.config import SQLALCHEMY_DATABASE_URL


@pytest.fixture(scope='module')
def temp_db():
    create_database(SQLALCHEMY_DATABASE_URL)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    alembic_cfg = Config(os.path.join(base_dir, 'alembic.ini'))
    command.upgrade(alembic_cfg, 'head')
    command.history(alembic_cfg)

    try:
        yield SQLALCHEMY_DATABASE_URL
    finally:
        drop_database(SQLALCHEMY_DATABASE_URL)
