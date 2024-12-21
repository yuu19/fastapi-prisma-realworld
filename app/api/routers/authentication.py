from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.schemas.user import UserInResponse, LoginUser, RegisterUser
from app.cruds.users import get_user_by_email
from app.core.config import settings
from datetime import timedelta
from app.core.security import create_access_token
from prisma.models import User
from app.api.deps import CurrentUser
from app.cruds.users import create_user
router = APIRouter()  

@router.post("/login", response_model=UserInResponse)
async def login(user: LoginUser = Body(..., embed=True)):
    user_db = await get_user_by_email(user.email)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": str(user_db.id)}, expires_delta=access_token_expires
    )
    return UserInResponse(**user_db.model_dump(), token=token)

@router.post("", response_model=UserInResponse)
async def register(user: RegisterUser = Body(..., embed=True)):
    user_db = await get_user_by_email(user.email)
    if user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    user_db = await create_user(user_create=user)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": str(user_db.id)}, expires_delta=access_token_expires
    )
    return UserInResponse(**user_db.model_dump(), token=token)