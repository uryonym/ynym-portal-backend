"""JWT トークン生成と検証."""

from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from app.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT アクセストークンを作成.

    Args:
        data: トークンにエンコードするデータ
        expires_delta: トークン有効期限

    Returns:
        JWT トークン文字列
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            hours=settings.jwt_expiration_hours
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def verify_token(token: str) -> dict:
    """JWT トークンを検証してデコード.

    Args:
        token: JWT トークン文字列

    Returns:
        デコードされたトークンデータ

    Raises:
        jwt.InvalidTokenError: トークンが無効または期限切れの場合
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except jwt.InvalidTokenError as e:
        raise jwt.InvalidTokenError(f"無効なトークン: {e}")
