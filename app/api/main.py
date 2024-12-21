from fastapi import APIRouter
from app.api.routers import authentication, articles, user, comment
#from app.api.routes import items, login, private, users, utils
#from app.core.config import settings

api_router = APIRouter()
# api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(authentication.router, prefix="/users", tags=["authentication"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(comment.router, prefix="/articles", tags=["comment"])