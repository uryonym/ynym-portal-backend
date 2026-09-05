from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import NullPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# エンジンを作成（コネクションプール無効）
engine = create_engine(settings.database_url, poolclass=NullPool)

# セッションファクトリを作成
session_local = sessionmaker(engine)


# セッション生成
def get_db() -> Generator[Session, None, None]:
    with session_local.begin() as session:
        yield session


# 互換性のためのエイリアス
get_session = get_db

# 依存関係注入用の型エイリアス
SessionDep = Annotated[Session, Depends(get_db)]
