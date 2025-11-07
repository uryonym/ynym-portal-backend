"""データベース接続とセッション管理."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings

# 非同期エンジンを作成
engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=settings.log_level == "DEBUG",
    future=True,
)

# 非同期セッションファクトリを作成
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """データベースセッション取得の依存性."""
    async with async_session_factory() as session:
        yield session
