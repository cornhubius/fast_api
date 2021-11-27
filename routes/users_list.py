from typing import List

from fastapi import APIRouter, Depends

from models.users import UserResponse
from repositories.users import UserRepository

from .depends import get_user_repository

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def read_users(
        users: UserRepository = Depends(get_user_repository),
        limit: int = 100,
        skip: int = 0):
    return await users.get_list_user(limit_show=limit, skip=skip)
