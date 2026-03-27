"""NoteCategoryService ユニットテスト（リポジトリをモック）."""

from unittest.mock import MagicMock
from uuid import UUID

import pytest

from app.models.note_category import NoteCategory
from app.repositories.note_category_repository import NoteCategoryRepository
from app.repositories.note_repository import NoteRepository
from app.schemas.note_category import NoteCategoryCreate, NoteCategoryUpdate
from app.services.note_category_service import NoteCategoryService
from app.utils.exceptions import NotFoundException

TEST_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")
CATEGORY_ID = UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")


@pytest.fixture
def mock_category_repo() -> MagicMock:
    repo = MagicMock(spec=NoteCategoryRepository)
    repo.save.side_effect = lambda obj: obj
    return repo


@pytest.fixture
def mock_note_repo() -> MagicMock:
    return MagicMock(spec=NoteRepository)


class TestNoteCategoryServiceListCategories:
    """list_categories テスト."""

    def test_returns_empty(self, mock_category_repo, mock_note_repo) -> None:
        """カテゴリなしで空リストを返す."""
        mock_category_repo.list_by_user.return_value = []
        service = NoteCategoryService(mock_category_repo, mock_note_repo)
        assert service.list_categories(TEST_USER_ID) == []

    def test_returns_categories(self, mock_category_repo, mock_note_repo) -> None:
        """複数カテゴリを返す."""
        c1 = MagicMock(spec=NoteCategory); c1.name = "仕事"
        c2 = MagicMock(spec=NoteCategory); c2.name = "趣味"
        mock_category_repo.list_by_user.return_value = [c1, c2]
        service = NoteCategoryService(mock_category_repo, mock_note_repo)
        result = service.list_categories(TEST_USER_ID)
        assert len(result) == 2
        assert result[0].name == "仕事"


class TestNoteCategoryServiceGetCategory:
    """get_category テスト."""

    def test_get_category_success(self, mock_category_repo, mock_note_repo) -> None:
        """カテゴリ取得成功."""
        category = MagicMock(spec=NoteCategory); category.id = CATEGORY_ID
        mock_category_repo.get_by_id_and_user.return_value = category
        service = NoteCategoryService(mock_category_repo, mock_note_repo)
        result = service.get_category(CATEGORY_ID, TEST_USER_ID)
        assert result.id == CATEGORY_ID

    def test_get_category_not_found(self, mock_category_repo, mock_note_repo) -> None:
        """カテゴリが見つからない場合 NotFoundException."""
        mock_category_repo.get_by_id_and_user.return_value = None
        service = NoteCategoryService(mock_category_repo, mock_note_repo)
        with pytest.raises(NotFoundException):
            service.get_category(CATEGORY_ID, TEST_USER_ID)


class TestNoteCategoryServiceCreateCategory:
    """create_category テスト."""

    def test_create_success(self, mock_category_repo, mock_note_repo) -> None:
        """カテゴリを作成できる."""
        service = NoteCategoryService(mock_category_repo, mock_note_repo)
        result = service.create_category(NoteCategoryCreate(name="仕事"), TEST_USER_ID)
        assert result.name == "仕事"
        assert result.user_id == TEST_USER_ID
        mock_category_repo.save.assert_called_once()


class TestNoteCategoryServiceUpdateCategory:
    """update_category テスト."""

    def test_update_name(self, mock_category_repo, mock_note_repo) -> None:
        """名前を更新できる."""
        category = NoteCategory(user_id=TEST_USER_ID, name="旧カテゴリ")
        mock_category_repo.get_by_id_and_user.return_value = category
        service = NoteCategoryService(mock_category_repo, mock_note_repo)
        result = service.update_category(CATEGORY_ID, NoteCategoryUpdate(name="新カテゴリ"), TEST_USER_ID)
        assert result.name == "新カテゴリ"

    def test_update_not_found_raises(self, mock_category_repo, mock_note_repo) -> None:
        """カテゴリが存在しない場合 NotFoundException."""
        mock_category_repo.get_by_id_and_user.return_value = None
        service = NoteCategoryService(mock_category_repo, mock_note_repo)
        with pytest.raises(NotFoundException):
            service.update_category(CATEGORY_ID, NoteCategoryUpdate(name="X"), TEST_USER_ID)


class TestNoteCategoryServiceDeleteCategory:
    """delete_category テスト."""

    def test_delete_nullifies_notes_and_deletes(self, mock_category_repo, mock_note_repo) -> None:
        """削除前に関連ノートのカテゴリを NULL にする."""
        category = MagicMock(spec=NoteCategory); category.id = CATEGORY_ID
        mock_category_repo.get_by_id_and_user.return_value = category
        service = NoteCategoryService(mock_category_repo, mock_note_repo)
        service.delete_category(CATEGORY_ID, TEST_USER_ID)
        mock_note_repo.nullify_category.assert_called_once_with(TEST_USER_ID, CATEGORY_ID)
        mock_category_repo.delete.assert_called_once_with(category)

    def test_delete_not_found_raises(self, mock_category_repo, mock_note_repo) -> None:
        """カテゴリが見つからない場合 NotFoundException."""
        mock_category_repo.get_by_id_and_user.return_value = None
        service = NoteCategoryService(mock_category_repo, mock_note_repo)
        with pytest.raises(NotFoundException):
            service.delete_category(CATEGORY_ID, TEST_USER_ID)
