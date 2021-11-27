from fastapi import APIRouter, Depends, HTTPException, status

from models.users import User, UserAuth, UserPatch, UserResponse
from repositories.users import UserRepository

from .depends import get_current_user, get_user_repository

router = APIRouter()


@router.get("/{id}", response_model=UserResponse)
async def get_users_by_id(id: int, users: UserRepository = Depends(get_user_repository)):
    return await users.get_by_id(id=id)


@router.delete("/{id}")
async def delete_user_by_id(
        id: int,
        users: UserRepository = Depends(get_user_repository),
        current_user: User = Depends(get_current_user)
):
    old_user = await users.get_by_id(id=id)
    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")
    return await users.delete(id=id)


@router.post("/", response_model=UserResponse)
async def create_user(user: UserAuth, users: UserRepository = Depends(get_user_repository)):
    return await users.create(user=user)


@router.put("/{id}", response_model=UserResponse)
async def update_user(
    id: int,
    user: UserAuth,
    users: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user)
):
    old_user = await users.get_by_id(id=id)
    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")
    return await users.update(id=id, user=user)


@router.patch("/{id}", response_model=UserResponse)
async def patch_user(
    id: int,
    user: UserPatch,
    users: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user)
):
    old_user = await users.get_by_id(id=id)
    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")
    return await users.patch(id=id, user=user)
