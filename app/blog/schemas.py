from typing import Optional, List

from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str
    user_id: int


class Blog(BlogBase):
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    blogs: List[Blog] = []

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    id: int
    title: str
    body: str
    creator: Optional[ShowUser] = None

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
