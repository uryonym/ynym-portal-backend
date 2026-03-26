"""NoteCategoryService のユニットテスト."""

from unittest.mock import MagicMock
from uuid import UUID

import pytest

from app.models.note_category import NoteCategory
from app.schemas.note_category import NoteCategoryCreate, NoteCategoryUpdate
from app.services.note_category_service import NoteCategoryService
from app.utils.exceptions import NotFoundException

TEST_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")


def create_mock_result(data: list) -> MagicMock:
    """SQLAlchemy 結果オブジェクトをモック."""
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = data

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    return mock_result


class TestNoteCategoryServiceListCategories:
    """NoteCategoryService.list_categories のテストケース."""

    @pytest.fixture
    def mock_db_session(self) -> MagicMock:
        return MagicMock()

    def test_list_categories_empty(self, mock_db_session: MagicMock) -> None:
        """カテゴリが存在しない場合、空リストを返す."""
        mock_db_session.execute = MagicMock(return_value=create_mock_result([]))

        service = NoteCategoryService(mock_db_session)
        categories = service.list_categories(TEST_USER_ID)

        assert categories == []
        mock_db_session.execute.assert_called_once()

    def test_list_categories_with_multiple(
        self, mock_db_session: MagicMock
    ) -> None:
        """複数カテゴリが存在する場合、カテゴリリストを返す."""
        category1 = MagicMock(spec=NoteCategory)
        category1.name = "仕事"

        category2 = MagicMock(spec=NoteCategory)
        category2.name = "個人"

        mock_db_session.execute = MagicMock(
            return_value=create_mock_result([category1, category2])
        )

        service = NoteCategoryService(mock_db_session)
        categories = service.list_categories(TEST_USER_ID)

        assert len(categories) == 2
        assert categories[0].name == "仕事"
        assert categories[1].name == "個人"


class TestNoteCategoryServiceGetCategory:
    """NoteCategoryService.get_category のテストケース."""

    @pytest.fixture
    def mock_db_session(self) -> MagicMock:
        return MagicMock()

    def test_get_category_success(self, mock_db_session: MagicMock) -> None:
        """カテゴリ取得成功."""
        category_id = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
        category = MagicMock(spec=NoteCategory)
        category.id = category_id

        mock_result = MagicMock()
        mock_result.scalars().one_or_none.return_value = category
        mock_db_session.execute.return_value = mock_result

        service = NoteCategoryService(mock_db_session)
        result = service.get_category(category_id, TEST_USER_ID)

        assert result.id == category_id

    def test_get_category_not_found(self, mock_db_session: MagicMock) -> None:
        """カテゴリが見つからない場合は例外."""
        category_id = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")

        mock_result = MagicMock()
        mock_result.scalars().one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result

        service = NoteCategoryService(mock_db_session)
        with pytest.raises(NotFoundException):
            service.get_category(category_id, TEST_USER_ID)


class TestNoteCategoryServiceCreateCategory:
    """NoteCategoryService.create_category のテストケース."""

    @pytest.fixture
    def mock_db_session(self) -> MagicMock:
        return MagicMock()

    def test_create_category_success(self, mock_db_session: MagicMock) -> None:
        """カテゴリ作成成功."""
        category_create = NoteCategoryCreate(name="仕事")

        mock_db_session.add = MagicMock()
        mock_db_session.commit = MagicMock()
        mock_db_session.refresh = MagicMock()

        service = NoteCategoryService(mock_db_session)
        result = service.create_category(category_create, TEST_USER_ID)

        assert result.user_id == TEST_USER_ID
        assert result.name == "仕事"
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()


class TestNoteCategoryServiceUpdateCategory:
    """NoteCategoryService.update_category のテストケース."""

    @pytest.fixture
    def mock_db_session(self) -> MagicMock:
        return MagicMock()

    def test_update_category_success(self, mock_db_session: MagicMock) -> None:
        """カテゴリ更新成功."""
        category_id = UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")
        category = MagicMock(spec=NoteCategory)
        category.id = category_id
        category.name = "旧カテゴリ"

        service = NoteCategoryService(mock_db_session)
        service.get_category = MagicMock(return_value=category)
        mock_db_session.commit = MagicMock()
        mock_db_session.refresh = MagicMock()

        category_update = NoteCategoryUpdate(name="新カテゴリ")
        updated = service.update_category(
            category_id, category_update, TEST_USER_ID
        )

        assert updated.name == "新カテゴリ"


class TestNoteCategoryServiceDeleteCategory:
    """NoteCategoryService.delete_category のテストケース."""

    @pytest.fixture
    def mock_db_session(self) -> MagicMock:
        return MagicMock()

    def test_delete_category_success(self, mock_db_session: MagicMock) -> None:
        """カテゴリ削除成功."""
        category_id = UUID("dddddddd-dddd-dddd-dddd-dddddddddddd")
        category = MagicMock(spec=NoteCategory)
        category.id = category_id

        service = NoteCategoryService(mock_db_session)
        service.get_category = MagicMock(return_value=category)
        mock_db_session.execute = MagicMock()
        mock_db_session.delete = MagicMock()
        mock_db_session.commit = MagicMock()

        service.delete_category(category_id, TEST_USER_ID)

        mock_db_session.execute.assert_called_once()
        mock_db_session.delete.assert_called_once_with(category)
        mock_db_session.commit.assert_called_once()
