from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from prisma.models import Article
 
from app.schemas.articles import CreateArticle, ArticleForResponse, ArticleInResponse,ArticleInUpdate
from app.schemas.profile import Profile
from app.cruds.articles import create_article, get_article_by_slug, delete_article_by_slug
from app.cruds.tags import create_tags_if_not_exist

from app.utils.articles import get_slug_for_article, check_article_exists_by_slug
from fastapi import Body
from prisma.partials import ArticleExcludeRelationFields
from app.api.deps import CurrentUser
from app.cruds.articles import update_article_by_slug
router = APIRouter()  

@router.post("", 
             status_code=status.HTTP_201_CREATED,
             response_model=ArticleInResponse
             )
async def create_new_article(user: CurrentUser, article_create: CreateArticle = Body(..., embed=True)):
    slug = get_slug_for_article(article_create.title)
    if await check_article_exists_by_slug(slug):
        raise HTTPException(status_code=400, detail="Article with this slug already exists")
    await create_tags_if_not_exist(tagLists=article_create.tagList)
    article = await create_article(slug=slug, title=article_create.title, description=article_create.description, body=article_create.body, author_id=user.id, tagList=article_create.tagList)
   
    article_for_response =  ArticleForResponse(**article.model_dump(), tag_list=article_create.tagList, 
                             author=Profile(
            username=user.username,
            bio=user.bio or "",
            image=user.image or "",
            following=False,  # 初期値(後で修正)
        ),)
    return ArticleInResponse(article=article_for_response) 


@router.put("/{slug}", 
             response_model=ArticleInResponse
             )
async def update_article(user: CurrentUser, slug: str, article_update: ArticleInUpdate = Body(..., embed=True)):
    article: Article = await get_article_by_slug(slug=slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the author of this article")
    return_tag_list = [tag.name for tag in article.tag_list]
    updated_article: ArticleExcludeRelationFields = await update_article_by_slug(slug=slug, title=article_update.title, description=article_update.description, body=article_update.body)
    article_for_response =  ArticleForResponse(**updated_article.model_dump(), tag_list=return_tag_list, 
                             author=Profile(
            username=user.username,
            bio=user.bio or "",
            image=user.image or "",
            following=False,  # 初期値(後で修正)
        ),)
    return ArticleInResponse(article=article_for_response) 


@router.delete("/{slug}", 
             status_code=status.HTTP_204_NO_CONTENT,
             )
async def delete_article(user: CurrentUser, slug: str):
    article = await get_article_by_slug(slug=slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the author of this article")
    await delete_article_by_slug(slug=slug)
    return None
  