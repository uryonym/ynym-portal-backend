"""TaskService.list_tasks() のユニットテスト."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID
from datetime import date, timedelta

from app.models.task import Task
from app.schemas.task import TaskCreate
from app.services.task_service import TaskService

# テスト用ユーザー ID（固定値）
TEST_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")


def create_mock_result(data: list) -> MagicMock:
    """SQLAlchemy 結果オブジェクトをモック.

    result = await session.execute(stmt)
    result.scalars().all() -> data
    """
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = data

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    return mock_result


class TestTaskServiceListTasks:
    """TaskService.list_tasks() のテストケース."""

    @pytest.fixture
    def mock_db_session(self):
        """モック DB セッション."""
        return AsyncMock()

    async def test_list_tasks_empty(self, mock_db_session) -> None:
        """タスクが存在しない場合、空リストを返す."""
        # モック設定: 空の結果
        mock_db_session.execute = AsyncMock(return_value=create_mock_result([]))

        # テスト実行
        service = TaskService(mock_db_session)
        tasks = await service.list_tasks(TEST_USER_ID)

        # 検証
        assert tasks == []
        mock_db_session.execute.assert_called_once()

    async def test_list_tasks_with_multiple_tasks(self, mock_db_session) -> None:
        """複数のタスクが存在する場合、タスクリストを返す."""
        # テストデータ作成
        task1 = MagicMock(spec=Task)
        task1.id = UUID("11111111-1111-1111-1111-111111111111")
        task1.title = "タスク1"

        task2 = MagicMock(spec=Task)
        task2.id = UUID("22222222-2222-2222-2222-222222222222")
        task2.title = "タスク2"

        # モック設定
        mock_db_session.execute = AsyncMock(return_value=create_mock_result([task1, task2]))

        # テスト実行
        service = TaskService(mock_db_session)
        tasks = await service.list_tasks(TEST_USER_ID)

        # 検証
        assert len(tasks) == 2
        assert tasks[0].title == "タスク1"
        assert tasks[1].title == "タスク2"

    async def test_list_tasks_sorting_by_due_date(self, mock_db_session) -> None:
        """期日でソートされることを確認（1番目のタスクが最も近い期日）."""
        # テストデータ: due_date が昇順でソートされていることをシミュレート
        today = date.today()

        task_earliest = MagicMock(spec=Task)
        task_earliest.due_date = today + timedelta(days=1)
        task_earliest.title = "最初の期日"

        task_middle = MagicMock(spec=Task)
        task_middle.due_date = today + timedelta(days=3)
        task_middle.title = "中間の期日"

        task_latest = MagicMock(spec=Task)
        task_latest.due_date = today + timedelta(days=5)
        task_latest.title = "最新の期日"

        # モック設定: nulls_last でソートされた順序で返す
        mock_db_session.execute = AsyncMock(
            return_value=create_mock_result([task_earliest, task_middle, task_latest])
        )

        # テスト実行
        service = TaskService(mock_db_session)
        tasks = await service.list_tasks(TEST_USER_ID)

        # 検証: 期日が昇順でソートされていることを確認
        assert len(tasks) == 3
        # 最初のタスクの期日が中間のタスクより早い、中間のタスクが最新のタスクより早い
        assert tasks[0].title == "最初の期日"
        assert tasks[1].title == "中間の期日"
        assert tasks[2].title == "最新の期日"

    async def test_list_tasks_undated_tasks_at_end(self, mock_db_session) -> None:
        """期日なしのタスクが期日ありのタスク後に表示される."""
        today = date.today()

        # 期日ありタスク
        task_with_due = MagicMock(spec=Task)
        task_with_due.due_date = today + timedelta(days=5)
        task_with_due.title = "期日ありタスク"

        # 期日なしタスク (NULL)
        task_without_due = MagicMock(spec=Task)
        task_without_due.due_date = None
        task_without_due.title = "期日なしタスク"

        # モック設定: nulls_last で期日ありが最初、期日なしが後
        mock_db_session.execute = AsyncMock(
            return_value=create_mock_result([task_with_due, task_without_due])
        )

        # テスト実行
        service = TaskService(mock_db_session)
        tasks = await service.list_tasks(TEST_USER_ID)

        # 検証: 期日ありが最初、期日なしが後
        assert len(tasks) == 2
        assert tasks[0].title == "期日ありタスク"
        assert tasks[0].due_date is not None
        assert tasks[1].title == "期日なしタスク"
        assert tasks[1].due_date is None


class TestTaskServiceCreateTask:
    """TaskService.create_task() のテストケース."""

    @pytest.fixture
    def mock_db_session(self):
        """モック DB セッション."""
        return AsyncMock()

    async def test_create_task_success(self, mock_db_session) -> None:
        """最小限のデータでタスク作成成功."""
        # テストデータ
        task_create = TaskCreate(
            title="買い物",
            description=None,
            due_date=None,
        )

        # 作成後のモック Task オブジェクト
        created_task = MagicMock(spec=Task)
        created_task.id = UUID("33333333-3333-3333-3333-333333333333")
        created_task.user_id = TEST_USER_ID
        created_task.title = "買い物"
        created_task.description = None
        created_task.is_completed = False
        created_task.due_date = None

        # モック設定: add, commit, refresh を無視
        mock_db_session.add = MagicMock()
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        # add の副作用として、task オブジェクトに id を設定するシミュレーション
        def add_side_effect(obj):
            obj.id = created_task.id
        mock_db_session.add.side_effect = add_side_effect

        # テスト実行
        service = TaskService(mock_db_session)
        result_task = await service.create_task(task_create, TEST_USER_ID)

        # 検証
        assert result_task.user_id == TEST_USER_ID
        assert result_task.title == "買い物"
        assert result_task.is_completed is False
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()

    async def test_create_task_with_all_fields(self, mock_db_session) -> None:
        """すべてのフィールドを指定してタスク作成成功."""
        # テストデータ
        due_date = date(2025, 12, 31)
        task_create = TaskCreate(
            title="年末大掃除",
            description="家中をキレイにする",
            due_date=due_date,
            is_completed=False,
        )

        # 作成後のモック Task オブジェクト
        created_task = MagicMock(spec=Task)
        created_task.id = UUID("44444444-4444-4444-4444-444444444444")
        created_task.user_id = TEST_USER_ID
        created_task.title = "年末大掃除"
        created_task.description = "家中をキレイにする"
        created_task.is_completed = False
        created_task.due_date = due_date

        # モック設定
        mock_db_session.add = MagicMock()
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()

        def add_side_effect(obj):
            obj.id = created_task.id
        mock_db_session.add.side_effect = add_side_effect

        # テスト実行
        service = TaskService(mock_db_session)
        result_task = await service.create_task(task_create, TEST_USER_ID)

        # 検証
        assert result_task.user_id == TEST_USER_ID
        assert result_task.title == "年末大掃除"
        assert result_task.description == "家中をキレイにする"
        assert result_task.is_completed is False
        assert result_task.due_date == due_date
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()
