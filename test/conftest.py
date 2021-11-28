import os
os.environ['TESTING'] = 'True'
from db import base
from sqlalchemy_utils import create_database, drop_database
from alembic.config import Config
from alembic import command

import pytest



@pytest.fixture(scope="module")
def temp_db():

    create_database(base.DATABASE_URL)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    command.upgrade(alembic_cfg, "head")

    try:
        yield base.DATABASE_URL
    finally:
        drop_database(base.DATABASE_URL)
