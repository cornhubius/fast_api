import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator

from exception.http_exception import PassDontMatch


class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: EmailStr
    password: str
    register_date: datetime.datetime


class UserResponse(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    register_date: Optional[datetime.datetime] = None


class UserPatch(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=8)] = None


class UserAuth(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=8)
    confirm_password: str

    @validator("confirm_password")
    def matching_passwords(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise PassDontMatch()
        return v
