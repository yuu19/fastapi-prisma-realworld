from app.prisma import prisma
from prisma.models import User
from app.schemas.user import RegisterUser
from app.schemas.user import UpdateUser
async def get_user_by_email(email: str) -> User:
    user: User = await prisma.user.find_first(where={"email": email})
    return user 

async def get_user_by_id(id: int) -> User:
    user: User = await prisma.user.find_unique_or_raise(where={"id": id})
    return user

async def create_user(user_create: RegisterUser) -> User:
    user  = await prisma.user.create(
        data={
            "email": user_create.email,
            "password": user_create.password,
            "username": user_create.username,
        }
    )
    return user

async def update_user(user: User, user_update: UpdateUser) -> User:
    user = await prisma.user.update(
        where={"id": user.id},
        data={
            "email": user_update.email or user.email,
            "username": user_update.username or user.username,
            "bio": user_update.bio or user.bio,
            "image": user_update.image or user.image,
        }
    )
    return user