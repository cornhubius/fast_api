import datetime
from typing import List, Optional

from fastapi import HTTPException, status

from core.security import hash_password
from db.users import users
from models.users import User, UserAuth, UserPatch, UserResponse

from .base import BaseRepository


class UserRepository(BaseRepository):
    async def get_list_user(self, limit_show: int = 100, skip: int = 0) -> List[User]:
        query = users.select().limit(limit_show).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Optional[User]:
        query = users.select().where(users.c.id == id)
        user = await self.database.fetch_one(query)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return User.parse_obj(user)

    async def create(self, user: UserAuth) -> Optional[User]:
        user = User(
            username=user.username,
            email=user.email,
            password=hash_password(user.password),
            register_date=datetime.datetime.utcnow(),
        )
        values = {**user.dict()}
        values.pop("id", None)
        try:
            query = users.insert().values(**values)
            user.id = await self.database.execute(query)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email must be unique")
        return user

    async def update(self, id: int, user: UserAuth) -> User:
        user_register_time = await self.database.fetch_one(users.select().where(users.c.id == id))
        user = User(
            id=id,
            username=user.username,
            email=user.email,
            password=hash_password(user.password),
            register_date={
                **User.parse_obj(user_register_time).dict()}['register_date'],
        )

        values = {**user.dict()}
        values.pop("id", None)

        query = users.update().where(users.c.id == id).values(**values)
        await self.database.execute(query)
        return user

    async def patch(self, id: int, user: UserPatch) -> Optional[User]:
        values = {**user.dict()}
        values = {k: v for k, v in values.items() if v is not None}
        if 'password' in values:
            values['password'] = hash_password(values['password'])
        query = users.update().where(users.c.id == id).values(values)
        if await self.database.execute(query=query) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Bad request')
        if 'id' not in values:
            values['id'] = id
        return UserPatch.parse_obj(values)

    async def delete(self, id: int):
        query = users.delete().where(users.c.id == id)
        await self.database.execute(query)
        return HTTPException(status_code=status.HTTP_200_OK, detail="Successful deleting")

    async def get_by_email(self, email: str) -> User:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)
