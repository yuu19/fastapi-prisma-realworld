import secrets
from typing import Any


from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",  # backendと同階層の.envファイルを読み込む
        env_ignore_empty=True,  # 環境変数が空の場合にエラーを発生させない
        extra="ignore",  # .envのみに存在する環境変数がある場合にエラーを発生させない
    )

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    API_STR: str = "/api"


settings = Settings()