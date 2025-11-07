"""パスワードハッシング・検証ユーティリティ."""

from passlib.context import CryptContext

# パスワードハッシング用コンテキストを作成
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """パスワードをハッシング.

    Args:
        password: プレーンテキストパスワード

    Returns:
        ハッシュ化されたパスワード
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワードをハッシュに対して検証.

    Args:
        plain_password: プレーンテキストパスワード
        hashed_password: ハッシュ化されたパスワード

    Returns:
        パスワードがマッチした場合は True、そうでない場合は False
    """
    return pwd_context.verify(plain_password, hashed_password)
