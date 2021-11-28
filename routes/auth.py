from fastapi import APIRouter, Depends
from fastapi.param_functions import Depends

from core.security import create_access_token, verify_password
from exception.http_exception import InvalidUsernameOrPassword
from models.token import Login, Token
from repositories.users import UserRepository

from .depends import get_user_repository

router = APIRouter()


@router.post("/", response_model=Token)
async def login(login: Login, users: UserRepository = Depends(get_user_repository)):
    user = await users.get_by_email(login.email)
    if user is None or not verify_password(login.password, user.password):
        raise InvalidUsernameOrPassword()
    return Token(
        access_token=create_access_token({"sub": user.email}),
        token_type="Bearer"

    )
