from slugify import slugify
from app.cruds.articles import get_article_by_slug 
from prisma.errors import RecordNotFoundError
async def check_article_exists_by_slug(slug: str) -> bool:
    try:
        await get_article_by_slug(slug=slug)
    except RecordNotFoundError as e:
        return False
    return True

def get_slug_for_article(title: str) -> str:
    return slugify(title) 


