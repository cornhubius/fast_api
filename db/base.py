from os import environ
import databases
from sqlalchemy import MetaData, create_engine
from starlette.config import Config
config = Config(".env")
TESTING = environ.get("TESTING")
if TESTING:
    DATABASE_URL = (config("TEST_DATABASE_URL", cast=str,
                    default="sqlite:///./test_sql_app.sqlite"))
    database = databases.Database(DATABASE_URL)
else:
    DATABASE_URL = (config("DATABASE_URL", cast=str,
                    default="sqlite:///./main_db.sqlite"))
    database = databases.Database(DATABASE_URL)

metadata = MetaData()
engine = create_engine(DATABASE_URL)
