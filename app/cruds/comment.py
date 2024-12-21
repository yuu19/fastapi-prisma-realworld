from prisma.models import Comment
from app.prisma import prisma

async def create_comment_prisma(*, body: str, article_id: int, author_id: int) -> Comment:
    comment = await prisma.comment.create(
        data={
            "body": body,
            "article_id": article_id,
            "author_id": author_id,
            "author": {
                "connect": {"id": author_id}
            },
        }
    )
    print("デバッグ: comment", comment)
    return comment