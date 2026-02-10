"""ノート/カテゴリ API エンドポイント統合テスト."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """FastAPI テストクライアント."""
    return TestClient(app)


class TestNoteEndpoints:
    """/api/notes エンドポイントのテスト."""

    def test_get_notes_list_empty(self, client: TestClient) -> None:
        """ノート一覧取得が正常に応答する."""
        response = client.get("/api/notes")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert data["message"] == "ノート一覧を取得しました"

    def test_post_notes_create_success(self, client: TestClient) -> None:
        """ノート作成が成功する."""
        payload = {
            "title": "新しいノート",
            "body": "本文",
        }
        response = client.post("/api/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "data" in data
        assert data["data"]["title"] == "新しいノート"
        assert data["data"]["body"] == "本文"
        assert data["message"] == "ノートが作成されました"


class TestNoteCategoryEndpoints:
    """/api/note-categories エンドポイントのテスト."""

    def test_get_note_categories_list_empty(self, client: TestClient) -> None:
        """カテゴリ一覧取得が正常に応答する."""
        response = client.get("/api/note-categories")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert data["message"] == "カテゴリ一覧を取得しました"

    def test_post_note_categories_create_success(self, client: TestClient) -> None:
        """カテゴリ作成が成功する."""
        payload = {
            "name": "仕事",
        }
        response = client.post("/api/note-categories", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "data" in data
        assert data["data"]["name"] == "仕事"
        assert data["message"] == "カテゴリが作成されました"
