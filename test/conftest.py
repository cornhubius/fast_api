import os
import pytest
os.environ['TESTING'] = 'True' #If we placed it below the application import, pytest will use main db
from alembic import command
from alembic.config import Config
from sqlalchemy_utils import create_database, drop_database
from fastapi.testclient import TestClient
from main import app
from db import base

client = TestClient(app)


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
