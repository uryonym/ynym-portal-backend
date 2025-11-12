"""タスク API エンドポイント統合テスト."""

import pytest
from fastapi.testclient import TestClient
from zoneinfo import ZoneInfo

from app.main import app

# 日本標準時 (JST)
JST = ZoneInfo("Asia/Tokyo")


@pytest.fixture
def client() -> TestClient:
    """FastAPI テストクライアント."""
    return TestClient(app)


class TestTaskListEndpoint:
    """GET /api/tasks エンドポイント統合テスト."""

    def test_get_tasks_list_empty(self, client: TestClient) -> None:
        """タスク一覧取得エンドポイントが正常に応答する."""
        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert "message" in data
        assert data["message"] == "タスク一覧を取得しました"

    def test_get_tasks_list_with_tasks(self) -> None:
        """タスク一覧取得で複数タスクが返されるケース."""
        # NOTE: asyncpg と TestClient の接続管理の制限により、
        # 同期テストクライアント内で複数の async DB 呼び出しは
        # "another operation is in progress" エラーが発生します。
        # 本格的なDB操作検証は、別途 async テストフレームワークで
        # 実装する必要があります (T020+ で実装予定)
        pass

    def test_get_tasks_sorting_correct(self) -> None:
        """タスク一覧がソートされることを検証."""
        # NOTE: ソート検証も同様に async テストが必要です
        pass

    def test_get_tasks_pagination_skip(self, client: TestClient) -> None:
        """skip クエリパラメータで最初の N 個をスキップ."""
        # TODO: ページネーション検証
        pass

    def test_get_tasks_pagination_limit(self, client: TestClient) -> None:
        """limit クエリパラメータで取得数を制限."""
        # TODO: ページネーション検証
        pass


class TestTaskCreateEndpoint:
    """POST /api/tasks エンドポイント統合テスト."""

    def test_post_tasks_create_success(self, client: TestClient) -> None:
        """有効なタスク作成リクエストで 201 ステータスと TaskResponse を返す."""
        payload = {
            "title": "新しいタスク",
            "description": "これはテストタスクです",
        }
        response = client.post("/api/tasks", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "data" in data
        task_response = data["data"]
        assert task_response["title"] == "新しいタスク"
        assert task_response["description"] == "これはテストタスクです"
        assert "id" in task_response
        assert "created_at" in task_response
        assert "updated_at" in task_response
        assert "message" in data
        assert data["message"] == "タスクが作成されました"

    def test_post_tasks_create_with_all_fields(self, client: TestClient) -> None:
        """すべてのフィールドを指定してタスク作成."""
        payload = {
            "title": "完全なタスク",
            "description": "すべてのフィールド付き",
            "due_date": "2025-12-31",
            "is_completed": False,
        }
        response = client.post("/api/tasks", json=payload)
        assert response.status_code == 201
        data = response.json()
        task_response = data["data"]
        assert task_response["title"] == "完全なタスク"
        assert task_response["due_date"] == "2025-12-31"
        assert task_response["is_completed"] is False

    def test_post_tasks_missing_title_fails(self, client: TestClient) -> None:
        """title を省略するとバリデーションエラー."""
        payload = {
            "description": "タイトルなしのタスク",
        }
        response = client.post("/api/tasks", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_post_tasks_title_empty_fails(self, client: TestClient) -> None:
        """title が空文字列の場合、バリデーションエラー."""
        payload = {
            "title": "",
            "description": "空のタイトル",
        }
        response = client.post("/api/tasks", json=payload)
        assert response.status_code == 422

    def test_post_tasks_title_too_long_fails(self, client: TestClient) -> None:
        """title が 255 文字を超える場合、バリデーションエラー."""
        payload = {
            "title": "a" * 256,
            "description": "長すぎるタイトル",
        }
        response = client.post("/api/tasks", json=payload)
        assert response.status_code == 422

    def test_post_tasks_description_too_long_fails(self, client: TestClient) -> None:
        """description が 2000 文字を超える場合、バリデーションエラー."""
        payload = {
            "title": "タスク",
            "description": "a" * 2001,
        }
        response = client.post("/api/tasks", json=payload)
        assert response.status_code == 422

    def test_post_tasks_created_at_is_jst(self, client: TestClient) -> None:
        """作成されたタスクの created_at が JST タイムスタンプ."""
        payload = {
            "title": "JST タスク",
        }
        response = client.post("/api/tasks", json=payload)
        assert response.status_code == 201
        data = response.json()
        task_response = data["data"]
        # created_at が ISO 8601 形式で返されることを確認
        assert "created_at" in task_response
        # TODO: timezone 検証を追加 (JST を確認)


class TestTaskGetByIdEndpoint:
    """GET /api/tasks/{task_id} エンドポイント統合テスト."""

    def test_get_task_by_id_success(self, client: TestClient) -> None:
        """タスク ID で特定のタスクを取得."""
        # TODO: テストデータ作成フィクスチャが必要
        pass

    def test_get_task_by_id_not_found(self, client: TestClient) -> None:
        """存在しないタスク ID で 404 を返す."""
        non_existent_id = "550e8400-e29b-41d4-a716-446655440099"
        response = client.get(f"/api/tasks/{non_existent_id}")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data or "message" in data


class TestTaskUpdateEndpoint:
    """PUT /api/tasks/{task_id} エンドポイント統合テスト."""

    def test_put_tasks_update_success(self, client: TestClient) -> None:
        """タスク更新で 200 ステータスと更新後のタスクを返す."""
        # TODO: テストデータ作成フィクスチャが必要
        pass

    def test_put_tasks_partial_update(self, client: TestClient) -> None:
        """部分更新: 指定されたフィールドのみ更新."""
        # TODO: テストデータ作成フィクスチャが必要
        pass

    def test_put_tasks_not_found_fails(self, client: TestClient) -> None:
        """存在しないタスク ID での更新で 404 を返す."""
        non_existent_id = "550e8400-e29b-41d4-a716-446655440099"
        payload = {
            "title": "更新されたタスク",
        }
        response = client.put(f"/api/tasks/{non_existent_id}", json=payload)
        assert response.status_code == 404


class TestTaskDeleteEndpoint:
    """DELETE /api/tasks/{task_id} エンドポイント統合テスト."""

    def test_delete_task_success(self, client: TestClient) -> None:
        """タスク削除で 204 No Content を返す."""
        # TODO: テストデータ作成フィクスチャが必要
        pass

    def test_delete_task_not_found_fails(self, client: TestClient) -> None:
        """存在しないタスク ID での削除で 404 を返す."""
        non_existent_id = "550e8400-e29b-41d4-a716-446655440099"
        response = client.delete(f"/api/tasks/{non_existent_id}")
        assert response.status_code == 404
