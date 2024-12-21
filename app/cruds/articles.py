from app.prisma import prisma
from prisma.models import Article
from typing import Sequence, Optional
from prisma.partials import ArticleExcludeRelationFields
from app.schemas.articles import ArticleInUpdate
from prisma import Prisma

async def get_article_by_slug(*, slug: str) -> Article:
    return await prisma.article.find_unique_or_raise(where={"slug": slug})

async def create_article(*, slug: str, 
                         title: str, 
                         description:str, 
                         body: str, 
                         author_id: int, 
                         tagList: Optional[Sequence[str]] = []
                         ) -> ArticleExcludeRelationFields:
    article = await prisma.article.create(
        data={
            "title": title, 
            "body": body, 
            "slug": slug, 
            "description": description,
            "author_id": author_id,
            "tag_list": {
                "connect": [{"name": tag} for tag in tagList]
            }
        },
        # include={
        #     "author": {
        #         "select": {
        #             "username": True,
        #             "bio": True,
        #             "image": True,
        #             "email": True
        #         }
        #     },
        # }
    )  
    return_article = ArticleExcludeRelationFields(**article.model_dump())
    return return_article

async def get_article_by_slug(*, slug: str) -> Article:
    return await prisma.article.find_unique(where={"slug": slug}, 
            include={"tag_list": True})

async def update_article_by_slug(*, slug: str, title: str | None, description: str | None,
                                 body: str | None) -> Article:
    article = await prisma.article.update(
        where={"slug": slug},
        data={
            "title": title,
            "description": description,
            "body": body
        }
    )

    return_article = ArticleExcludeRelationFields(**article.model_dump())
    return return_article
    

async def delete_article_by_slug(*, slug: str) -> None:
    await prisma.article.delete(where={"slug": slug})