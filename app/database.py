"""データベース接続とセッション管理."""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.core.config import settings

# 同期エンジンを作成
engine = create_engine(
    settings.database_url,
    echo=settings.LOG_LEVEL == "DEBUG",
)

# セッションファクトリを作成
session_factory = sessionmaker(engine, class_=Session, expire_on_commit=False)


def get_session() -> Generator[Session, None, None]:
    """データベースセッション取得の依存性."""
    with session_factory() as session:
        yield session
