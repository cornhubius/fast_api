from starlette.config import Config

config = Config(".env")

ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"
SECRET_KEY = config("EE_SECRET_KEY", cast=str,
                    default='bceb4aead50411deb8453a3d17af88a33aba1e99f68f0626f00100329250d0c0')
