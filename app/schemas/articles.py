from typing import List, Optional
from pydantic import BaseModel
from app.schemas.profile import Profile
from datetime import datetime   

class CreateArticle(BaseModel):
    title: str
    description: str
    body: str
    tagList: Optional[List[str]] = None

class ArticleForResponse(BaseModel):
    id: int = 0
    slug: str
    title: str
    description: str
    body: str
    tag_list: List[str]
    created_at: datetime
    updated_at: datetime
    favorited: bool = False #とりあえずデフォルト値を設定
    favorites_count: int = 0 #とりあえずデフォルト値を設定
    author: Profile

class ArticleInResponse(BaseModel):
    article: ArticleForResponse

class ArticleInUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None