from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


# class UpdatePost(PostBase):
#     title: str
#     content: str
#     published: bool
class UserResponse(BaseModel):
    email_address: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    # owner: UserResponse

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email_address: EmailStr
    password: str

    class Config:
        orm_mode = True


class SingleUserResponse(BaseModel):
    email_address: EmailStr
    id: int

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    token: str
    type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
