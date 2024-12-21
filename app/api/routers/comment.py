from fastapi import APIRouter
from app.schemas.comment import CommentInResponse, CommentForResponse, CommentInCreate
from app.api.deps import CurrentUser
from app.cruds.articles import get_article_by_slug
from app.cruds.comment import create_comment_prisma
from fastapi import HTTPException
router = APIRouter() 

@router.post("/{slug}/comments", response_model=CommentInResponse)
async def create_comment(*, user: CurrentUser, slug: str, comment_create: CommentInCreate):
    try: 
        db_comment = await get_article_by_slug(slug=slug)
        author_id = db_comment.author_id
    except:
        raise HTTPException(status_code=404, detail="Article not found")
    comment = await create_comment_prisma(body=comment_create.body, article_id=author_id, author_id=user.id)
    comment_for = CommentForResponse(**comment.model_dump())
    return CommentInResponse(comment=comment_for)
