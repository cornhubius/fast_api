from starlette.config import Config

config = Config(".env")

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=60)
ALGORITHM = config("ALGORITHM", default="HS256")
SECRET_KEY = config("EE_SECRET_KEY", default="SeretKey")
