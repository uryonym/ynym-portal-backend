"""タスクスキーマのユニットテスト."""

from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.task import TaskCreate, TaskUpdate


class TestTaskCreateSchema:
    """TaskCreate スキーマのバリデーションテスト."""

    def test_task_create_valid_with_all_fields(self) -> None:
        """すべてのフィールドが有効な場合、タスク作成成功."""
        task_data = TaskCreate(
            title="買い物",
            description="牛乳を買う",
            due_date=date(2025, 11, 20),
            is_completed=False,
        )
        assert task_data.title == "買い物"
        assert task_data.description == "牛乳を買う"
        assert task_data.due_date == date(2025, 11, 20)
        assert task_data.is_completed is False

    def test_task_create_valid_with_minimal_fields(self) -> None:
        """必須フィールドのみでタスク作成成功."""
        task_data = TaskCreate(title="テスト")
        assert task_data.title == "テスト"
        assert task_data.description is None
        assert task_data.due_date is None
        assert task_data.is_completed is False

    def test_task_create_title_required(self) -> None:
        """title が必須フィールドの場合、省略するとバリデーションエラー."""
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="")  # type: ignore
        errors = exc_info.value.errors()
        assert len(errors) > 0

    def test_task_create_title_empty_fails(self) -> None:
        """title が空文字列の場合、バリデーションエラー."""
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="")
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("title",) for error in errors)

    def test_task_create_title_whitespace_only_fails(self) -> None:
        """title が空白文字のみの場合、バリデーションエラー."""
        with pytest.raises(ValidationError):
            TaskCreate(title="   ")

    def test_task_create_title_too_long_fails(self) -> None:
        """title が 255 文字を超える場合、バリデーションエラー."""
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="a" * 256)
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("title",) for error in errors)

    def test_task_create_title_max_length_valid(self) -> None:
        """title が正確に 255 文字の場合、バリデーション成功."""
        task_data = TaskCreate(title="a" * 255)
        assert len(task_data.title) == 255

    def test_task_create_description_empty_valid(self) -> None:
        """description が空文字列の場合、None に変換される."""
        task_data = TaskCreate(title="テスト", description="")
        assert task_data.description is None

    def test_task_create_description_too_long_fails(self) -> None:
        """description が 2000 文字を超える場合、バリデーションエラー."""
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="テスト", description="a" * 2001)
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("description",) for error in errors)

    def test_task_create_description_max_length_valid(self) -> None:
        """description が正確に 2000 文字の場合、バリデーション成功."""
        task_data = TaskCreate(title="テスト", description="a" * 2000)
        assert task_data.description is not None
        assert len(task_data.description) == 2000

    def test_task_create_title_whitespace_trimmed(self) -> None:
        """title の前後の空白が自動的にトリミングされる."""
        task_data = TaskCreate(title="  テスト  ")
        assert task_data.title == "テスト"

    def test_task_create_description_whitespace_trimmed(self) -> None:
        """description の前後の空白が自動的にトリミングされる."""
        task_data = TaskCreate(title="テスト", description="  説明  ")
        assert task_data.description == "説明"


class TestTaskUpdateSchema:
    """TaskUpdate スキーマのバリデーションテスト."""

    def test_task_update_all_fields_optional(self) -> None:
        """すべてのフィールドがオプションなので、空のオブジェクト生成成功."""
        task_data = TaskUpdate()
        assert task_data.title is None
        assert task_data.description is None
        assert task_data.is_completed is None
        assert task_data.due_date is None

    def test_task_update_partial_update_title_only(self) -> None:
        """title のみ更新可能."""
        task_data = TaskUpdate(title="新しいタイトル")
        assert task_data.title == "新しいタイトル"
        assert task_data.description is None
        assert task_data.is_completed is None

    def test_task_update_title_empty_fails(self) -> None:
        """title が空文字列の場合、バリデーションエラー."""
        with pytest.raises(ValidationError) as exc_info:
            TaskUpdate(title="")
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("title",) for error in errors)

    def test_task_update_title_too_long_fails(self) -> None:
        """title が 255 文字を超える場合、バリデーションエラー."""
        with pytest.raises(ValidationError) as exc_info:
            TaskUpdate(title="a" * 256)
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("title",) for error in errors)

    def test_task_update_description_empty_valid(self) -> None:
        """description が空文字列の場合、None に変換される."""
        task_data = TaskUpdate(description="")
        assert task_data.description is None

    def test_task_update_description_too_long_fails(self) -> None:
        """description が 2000 文字を超える場合、バリデーションエラー."""
        with pytest.raises(ValidationError) as exc_info:
            TaskUpdate(description="a" * 2001)
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("description",) for error in errors)

    def test_task_update_is_completed_true(self) -> None:
        """is_completed を True で更新可能."""
        task_data = TaskUpdate(is_completed=True)
        assert task_data.is_completed is True

    def test_task_update_is_completed_false(self) -> None:
        """is_completed を False で更新可能."""
        task_data = TaskUpdate(is_completed=False)
        assert task_data.is_completed is False

    def test_task_update_multiple_fields(self) -> None:
        """複数フィールドを同時に更新可能."""
        task_data = TaskUpdate(
            title="新しいタイトル",
            description="新しい説明",
            is_completed=True,
            due_date=date(2025, 12, 1),
        )
        assert task_data.title == "新しいタイトル"
        assert task_data.description == "新しい説明"
        assert task_data.is_completed is True
        assert task_data.due_date == date(2025, 12, 1)


class TestTaskValidationEdgeCases:
    """バリデーションのエッジケーステスト."""

    def test_task_create_title_single_character(self) -> None:
        """title が 1 文字の場合、バリデーション成功."""
        task_data = TaskCreate(title="a")
        assert task_data.title == "a"

    def test_task_create_description_single_character(self) -> None:
        """description が 1 文字の場合、バリデーション成功."""
        task_data = TaskCreate(title="テスト", description="a")
        assert task_data.description == "a"

    def test_task_create_unicode_title(self) -> None:
        """title が Unicode 文字を含む場合、バリデーション成功."""
        task_data = TaskCreate(title="日本語のタスク")
        assert task_data.title == "日本語のタスク"

    def test_task_create_special_characters_title(self) -> None:
        """title が特殊文字を含む場合、バリデーション成功."""
        task_data = TaskCreate(title="タスク!@#$%^&*()")
        assert task_data.title == "タスク!@#$%^&*()"

    def test_task_update_title_none_valid(self) -> None:
        """TaskUpdate で title が None の場合、バリデーション成功."""
        task_data = TaskUpdate(title=None)
        assert task_data.title is None
