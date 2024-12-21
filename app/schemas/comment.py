from app.schemas.profile import Profile
from datetime import datetime
from pydantic import BaseModel

class CommentInCreate(BaseModel):
    body: str

class CommentForResponse(BaseModel):
    id: int
    createdAt: datetime
    updatedAt: datetime
    body: str
    author: Profile

class CommentInResponse(BaseModel):
    comment: CommentForResponse    