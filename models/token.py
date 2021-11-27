from pydantic import BaseModel
from pydantic.networks import EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class Login(BaseModel):
    email: EmailStr
    password: str
