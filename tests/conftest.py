"""pytest 設定と fixture."""

from datetime import datetime
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.database import get_session
from app.main import app
from app.models.base import Base, JST
from app.models.user import User
from app.security.deps import get_current_user

# SQLite in-memory エンジン（テスト用）
TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
)

# SQLite の外部キー制約を有効化
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, _):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """テストセッション開始時にテーブルを作成し、終了時に削除."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """テスト用 DB セッション（各テスト後にロールバック）."""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


def _override_current_user() -> User:
    return User(
        id=UUID("550e8400-e29b-41d4-a716-446655440000"),
        email="test@example.com",
        name="テストユーザー",
        avatar_url=None,
        created_at=datetime.now(JST),
        updated_at=datetime.now(JST),
    )


@pytest.fixture
def client(db_session: Session) -> TestClient:
    """FastAPI テストクライアント（SQLite in-memory DB + 認証モック）."""

    def _override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = _override_get_session
    app.dependency_overrides[get_current_user] = _override_current_user
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.pop(get_session, None)
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture(autouse=True)
def override_current_user_dependency():
    """認証依存をテスト用ユーザーで上書き（client fixture 未使用のテスト向け）."""
    app.dependency_overrides[get_current_user] = _override_current_user
    yield
    app.dependency_overrides.pop(get_current_user, None)
