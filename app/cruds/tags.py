from app.prisma import prisma


async def create_tags_if_not_exist(*, tagLists: str) -> dict:
  for tag in tagLists:
    await prisma.tag.upsert(
      where={
        'name': tag
      },
      data={
        'create': {
          'name': tag
        },
        'update': {}
      }
    )

