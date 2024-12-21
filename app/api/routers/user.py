from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from prisma.models import Article
 
from app.schemas.articles import CreateArticle, ArticleForResponse, ArticleInResponse,ArticleInUpdate
from app.schemas.profile import Profile
from app.schemas.user import UserInResponse
from app.cruds.articles import create_article, get_article_by_slug, delete_article_by_slug
from app.cruds.tags import create_tags_if_not_exist
from app.cruds.users import update_user
router = APIRouter()  
from app.utils.articles import get_slug_for_article, check_article_exists_by_slug
from fastapi import Body
from prisma.partials import ArticleExcludeRelationFields
from app.api.deps import CurrentUser
from app.cruds.articles import update_article_by_slug

from app.schemas.user import UserInResponse, UpdateUser

router = APIRouter()  

@router.get("/", response_model=UserInResponse)
async def get_current_user(user: CurrentUser):
    return UserInResponse(**user.model_dump())

@router.put("/", response_model=UserInResponse)
async def update_current_user(user: CurrentUser, user_update: UpdateUser = Body(..., embed=True)):
    user = await update_user(user=user, user_update=user_update)
    return UserInResponse(**user.model_dump())