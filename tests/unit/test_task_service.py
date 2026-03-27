"""TaskService ユニットテスト（TaskRepository をモック）."""

from datetime import date, timedelta
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import TaskService
from app.utils.exceptions import NotFoundException

TEST_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")


# ---------------------------------------------------------------------------
# ヘルパー
# ---------------------------------------------------------------------------

def _make_task(**kwargs) -> Task:
    """テスト用 Task オブジェクトを生成."""
    defaults = dict(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        user_id=TEST_USER_ID,
        title="デフォルトタスク",
        description=None,
        is_completed=False,
        due_date=None,
        deleted_at=None,
        order=0,
    )
    defaults.update(kwargs)
    task = MagicMock(spec=Task)
    for k, v in defaults.items():
        setattr(task, k, v)
    return task


# ---------------------------------------------------------------------------
# list_tasks
# ---------------------------------------------------------------------------

class TestTaskServiceListTasks:
    """TaskService.list_tasks() テストケース."""

    @pytest.fixture
    def mock_repo(self) -> MagicMock:
        return MagicMock(spec=TaskRepository)

    def test_returns_empty_list_when_no_tasks(self, mock_repo: MagicMock) -> None:
        """タスクなしで空リストを返す."""
        mock_repo.list_by_user.return_value = []
        service = TaskService(mock_repo)
        result = service.list_tasks(TEST_USER_ID)
        assert result == []
        mock_repo.list_by_user.assert_called_once_with(TEST_USER_ID, 0, 100, None)

    def test_returns_all_tasks(self, mock_repo: MagicMock) -> None:
        """複数タスクを返す."""
        tasks = [_make_task(title="A"), _make_task(title="B")]
        mock_repo.list_by_user.return_value = tasks
        service = TaskService(mock_repo)
        result = service.list_tasks(TEST_USER_ID)
        assert len(result) == 2

    def test_passes_is_completed_filter(self, mock_repo: MagicMock) -> None:
        """is_completed フィルタがリポジトリに渡される."""
        mock_repo.list_by_user.return_value = []
        service = TaskService(mock_repo)
        service.list_tasks(TEST_USER_ID, is_completed=False)
        mock_repo.list_by_user.assert_called_once_with(TEST_USER_ID, 0, 100, False)

    def test_passes_pagination_params(self, mock_repo: MagicMock) -> None:
        """skip/limit がリポジトリに渡される."""
        mock_repo.list_by_user.return_value = []
        service = TaskService(mock_repo)
        service.list_tasks(TEST_USER_ID, skip=10, limit=5)
        mock_repo.list_by_user.assert_called_once_with(TEST_USER_ID, 10, 5, None)


# ---------------------------------------------------------------------------
# get_task
# ---------------------------------------------------------------------------

class TestTaskServiceGetTask:
    """TaskService.get_task() テストケース."""

    @pytest.fixture
    def mock_repo(self) -> MagicMock:
        return MagicMock(spec=TaskRepository)

    def test_returns_task_when_found(self, mock_repo: MagicMock) -> None:
        """タスクが存在する場合に返す."""
        task = _make_task()
        mock_repo.get_by_id_and_user.return_value = task
        service = TaskService(mock_repo)
        result = service.get_task(task.id, TEST_USER_ID)
        assert result is task

    def test_raises_not_found_when_missing(self, mock_repo: MagicMock) -> None:
        """タスクが存在しない場合 NotFoundException を発生させる."""
        mock_repo.get_by_id_and_user.return_value = None
        service = TaskService(mock_repo)
        with pytest.raises(NotFoundException):
            service.get_task(UUID("99999999-9999-9999-9999-999999999999"), TEST_USER_ID)


# ---------------------------------------------------------------------------
# create_task
# ---------------------------------------------------------------------------

class TestTaskServiceCreateTask:
    """TaskService.create_task() テストケース."""

    @pytest.fixture
    def mock_repo(self) -> MagicMock:
        repo = MagicMock(spec=TaskRepository)
        # save はそのまま渡したオブジェクトを返す
        repo.save.side_effect = lambda task: task
        return repo

    def test_create_minimal(self, mock_repo: MagicMock) -> None:
        """最小フィールドでタスクを作成."""
        task_create = TaskCreate(title="買い物")
        service = TaskService(mock_repo)
        result = service.create_task(task_create, TEST_USER_ID)
        assert result.user_id == TEST_USER_ID
        assert result.title == "買い物"
        assert result.is_completed is False
        mock_repo.save.assert_called_once()

    def test_create_with_all_fields(self, mock_repo: MagicMock) -> None:
        """すべてのフィールドを指定してタスクを作成."""
        due = date(2025, 12, 31)
        task_create = TaskCreate(title="年末大掃除", description="家中をキレイにする", due_date=due)
        service = TaskService(mock_repo)
        result = service.create_task(task_create, TEST_USER_ID)
        assert result.title == "年末大掃除"
        assert result.description == "家中をキレイにする"
        assert result.due_date == due

    def test_title_empty_raises_validation_error(self) -> None:
        """タイトルが空文字列で ValidationError."""
        with pytest.raises(ValidationError):
            TaskCreate(title="")

    def test_title_too_long_raises_validation_error(self) -> None:
        """タイトルが 256 文字で ValidationError."""
        with pytest.raises(ValidationError):
            TaskCreate(title="a" * 256)

    def test_description_too_long_raises_validation_error(self) -> None:
        """description が 2001 文字で ValidationError."""
        with pytest.raises(ValidationError):
            TaskCreate(title="タスク", description="a" * 2001)


# ---------------------------------------------------------------------------
# update_task
# ---------------------------------------------------------------------------

class TestTaskServiceUpdateTask:
    """TaskService.update_task() テストケース."""

    @pytest.fixture
    def mock_repo(self) -> MagicMock:
        repo = MagicMock(spec=TaskRepository)
        repo.save.side_effect = lambda task: task
        return repo

    def test_update_title(self, mock_repo: MagicMock) -> None:
        """タイトルを更新できる."""
        task = Task(
            id=UUID("22222222-2222-2222-2222-222222222222"),
            user_id=TEST_USER_ID,
            title="古いタイトル",
            is_completed=False,
        )
        mock_repo.get_by_id_and_user.return_value = task
        service = TaskService(mock_repo)
        result = service.update_task(task.id, TaskUpdate(title="新しいタイトル"), TEST_USER_ID)
        assert result.title == "新しいタイトル"
        mock_repo.save.assert_called_once()

    def test_complete_task_sets_completed_at(self, mock_repo: MagicMock) -> None:
        """is_completed を True に変更すると completed_at が設定される."""
        task = Task(
            id=UUID("22222222-2222-2222-2222-222222222222"),
            user_id=TEST_USER_ID,
            title="タスク",
            is_completed=False,
            completed_at=None,
        )
        mock_repo.get_by_id_and_user.return_value = task
        service = TaskService(mock_repo)
        result = service.update_task(task.id, TaskUpdate(is_completed=True), TEST_USER_ID)
        assert result.is_completed is True
        assert result.completed_at is not None

    def test_uncomplete_task_clears_completed_at(self, mock_repo: MagicMock) -> None:
        """is_completed を False に変更すると completed_at がクリアされる."""
        from datetime import datetime
        from app.models.base import JST
        task = Task(
            id=UUID("22222222-2222-2222-2222-222222222222"),
            user_id=TEST_USER_ID,
            title="タスク",
            is_completed=True,
            completed_at=datetime.now(JST),
        )
        mock_repo.get_by_id_and_user.return_value = task
        service = TaskService(mock_repo)
        result = service.update_task(task.id, TaskUpdate(is_completed=False), TEST_USER_ID)
        assert result.is_completed is False
        assert result.completed_at is None

    def test_update_not_found_raises(self, mock_repo: MagicMock) -> None:
        """タスクが存在しない場合 NotFoundException を発生させる."""
        mock_repo.get_by_id_and_user.return_value = None
        service = TaskService(mock_repo)
        with pytest.raises(NotFoundException):
            service.update_task(UUID("99999999-9999-9999-9999-999999999999"), TaskUpdate(title="X"), TEST_USER_ID)


# ---------------------------------------------------------------------------
# delete_task
# ---------------------------------------------------------------------------

class TestTaskServiceDeleteTask:
    """TaskService.delete_task() テストケース."""

    @pytest.fixture
    def mock_repo(self) -> MagicMock:
        return MagicMock(spec=TaskRepository)

    def test_delete_existing_task(self, mock_repo: MagicMock) -> None:
        """タスクを正常に削除できる."""
        task = _make_task()
        mock_repo.get_by_id_and_user.return_value = task
        service = TaskService(mock_repo)
        service.delete_task(task.id, TEST_USER_ID)
        mock_repo.delete.assert_called_once_with(task)

    def test_delete_not_found_raises(self, mock_repo: MagicMock) -> None:
        """タスクが見つからない場合 NotFoundException を発生させる."""
        mock_repo.get_by_id_and_user.return_value = None
        service = TaskService(mock_repo)
        with pytest.raises(NotFoundException):
            service.delete_task(UUID("99999999-9999-9999-9999-999999999999"), TEST_USER_ID)
