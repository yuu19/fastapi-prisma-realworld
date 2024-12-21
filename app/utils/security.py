import jwt
from pydantic import ValidationError
from app.core.config import settings
#Todo: エラー処理等を見直す
def get_username_from_token(token: str, secret_key: str) -> str:
    try:
        decoded = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
        return decoded["username"]
    except jwt.PyJWTError as decode_error:
        raise ValueError("unable to decode JWT token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("malformed payload in token") from validation_error
    except Exception as e:
        raise ValueError("unable to get username from token") from e