"""pytest 設定と fixture."""

import pytest
from fastapi.testclient import TestClient
from datetime import date, datetime
from zoneinfo import ZoneInfo
from uuid import UUID

from app.main import app
from app.models.base import JST
from app.models.user import User
from app.security.deps import get_current_user

# 日本標準時 (JST)
JST = ZoneInfo("Asia/Tokyo")


@pytest.fixture
def client():
    """FastAPI テストクライアント."""
    return TestClient(app)


@pytest.fixture
def sample_task_data() -> dict:
    """テスト用タスクデータ."""
    return {
        "user_id": UUID("550e8400-e29b-41d4-a716-446655440000"),
        "title": "テストタスク",
        "description": "テストタスクの説明",
        "is_completed": False,
        "due_date": date(2025, 12, 31),
    }


@pytest.fixture
def task_fixtures() -> dict:
    """
    テスト用タスクフィクスチャデータセット.

    3 つのテストタスク：
    - task_with_due_date: 期日あり、未完了
    - task_without_due_date: 期日なし、未完了
    - task_completed: 完了済みタスク
    """
    return {
        "task_with_due_date": {
            "user_id": UUID("550e8400-e29b-41d4-a716-446655440000"),
            "title": "期日ありのタスク",
            "description": "期日が設定されているテストタスク",
            "is_completed": False,
            "due_date": date(2025, 11, 30),
        },
        "task_without_due_date": {
            "user_id": UUID("550e8400-e29b-41d4-a716-446655440000"),
            "title": "期日なしのタスク",
            "description": "期日が設定されていないテストタスク",
            "is_completed": False,
            "due_date": None,
        },
        "task_completed": {
            "user_id": UUID("550e8400-e29b-41d4-a716-446655440000"),
            "title": "完了済みタスク",
            "description": "すでに完了しているテストタスク",
            "is_completed": True,
            "due_date": date(2025, 11, 15),
        },
    }


@pytest.fixture(autouse=True)
def override_current_user_dependency():
    """認証依存をテスト用ユーザーで上書き."""

    def _override_current_user() -> User:
        return User(
            id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            email="test@example.com",
            name="テストユーザー",
            avatar_url=None,
            created_at=datetime.now(JST),
        )

    app.dependency_overrides[get_current_user] = _override_current_user
    yield
    app.dependency_overrides.pop(get_current_user, None)
