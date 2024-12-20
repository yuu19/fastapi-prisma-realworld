# generated by datamodel-codegen:
#   filename:  openapi.yml
#   timestamp: 2024-12-05T01:24:23+00:00

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, SecretStr


class LoginUser(BaseModel):
    email: str
    password: SecretStr


class NewUser(BaseModel):
    username: str
    email: str
    password: SecretStr


class User(BaseModel):
    email: str
    token: str
    username: str
    bio: str
    image: str


class UpdateUser(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None


class Profile(BaseModel):
    username: str
    bio: str
    image: str
    following: bool


class Article(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tagList: List[str]
    createdAt: datetime
    updatedAt: datetime
    favorited: bool
    favoritesCount: int
    author: Profile


class NewArticle(BaseModel):
    title: str
    description: str
    body: str
    tagList: Optional[List[str]] = None


class UpdateArticle(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None


class Comment(BaseModel):
    id: int
    createdAt: datetime
    updatedAt: datetime
    body: str
    author: Profile


class NewComment(BaseModel):
    body: str


class Errors(BaseModel):
    body: List[str]


class GenericErrorModel(BaseModel):
    errors: Errors
