# from debug_toolbar.panels.sqlalchemy import SQLAlchemyPanel as BasePanel
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status

# from api.main import DEBUG
from fastapi.security import OAuth2PasswordBearer

# from jose import jwt
from jwt.exceptions import InvalidTokenError

# from jwt import InvalidTokenError
from pydantic import ValidationError

from app.cruds.users import get_user_by_email, get_user_by_id
from app.core.config import settings
from prisma.models import User
from app.schemas.user import TokenPayload
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from app.schemas.users import TokenPayload, User
from fastapi import Security
from prisma.errors import RecordNotFoundError
security = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Security(security)
) -> User:
    try:
        payload = jwt.decode(
            token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    # 署名が一致しない場合、有効期限切れの場合、有効なペイロードでない場合
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    try:
        user = await get_user_by_id(int(token_data.sub))
    except RecordNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


