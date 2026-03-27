"""NoteService ユニットテスト（リポジトリをモック）."""

from unittest.mock import MagicMock
from uuid import UUID

import pytest

from app.models.note import Note
from app.repositories.note_category_repository import NoteCategoryRepository
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate
from app.services.note_service import NoteService
from app.utils.exceptions import NotFoundException

TEST_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")
NOTE_ID = UUID("11111111-1111-1111-1111-111111111111")
CATEGORY_ID = UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")


@pytest.fixture
def mock_note_repo() -> MagicMock:
    repo = MagicMock(spec=NoteRepository)
    repo.save.side_effect = lambda obj: obj
    return repo


@pytest.fixture
def mock_category_repo() -> MagicMock:
    return MagicMock(spec=NoteCategoryRepository)


class TestNoteServiceListNotes:
    """list_notes テスト."""

    def test_returns_empty(self, mock_note_repo, mock_category_repo) -> None:
        """ノートなしで空リストを返す."""
        mock_note_repo.list_by_user.return_value = []
        service = NoteService(mock_note_repo, mock_category_repo)
        assert service.list_notes(TEST_USER_ID) == []

    def test_returns_notes(self, mock_note_repo, mock_category_repo) -> None:
        """複数ノートを返す."""
        n1 = MagicMock(spec=Note); n1.title = "ノート1"
        n2 = MagicMock(spec=Note); n2.title = "ノート2"
        mock_note_repo.list_by_user.return_value = [n1, n2]
        service = NoteService(mock_note_repo, mock_category_repo)
        result = service.list_notes(TEST_USER_ID)
        assert len(result) == 2
        assert result[0].title == "ノート1"


class TestNoteServiceGetNote:
    """get_note テスト."""

    def test_get_note_success(self, mock_note_repo, mock_category_repo) -> None:
        """ノート取得成功."""
        note = MagicMock(spec=Note); note.id = NOTE_ID
        mock_note_repo.get_by_id_and_user.return_value = note
        service = NoteService(mock_note_repo, mock_category_repo)
        result = service.get_note(NOTE_ID, TEST_USER_ID)
        assert result.id == NOTE_ID

    def test_not_found_raises(self, mock_note_repo, mock_category_repo) -> None:
        """存在しないノートで NotFoundException."""
        mock_note_repo.get_by_id_and_user.return_value = None
        service = NoteService(mock_note_repo, mock_category_repo)
        with pytest.raises(NotFoundException):
            service.get_note(NOTE_ID, TEST_USER_ID)


class TestNoteServiceCreateNote:
    """create_note テスト."""

    def test_create_without_category(self, mock_note_repo, mock_category_repo) -> None:
        """カテゴリなしでノート作成."""
        note_create = NoteCreate(title="タイトル", body="本文")
        service = NoteService(mock_note_repo, mock_category_repo)
        result = service.create_note(note_create, TEST_USER_ID)
        assert result.title == "タイトル"
        assert result.body == "本文"
        mock_category_repo.get_by_id_and_user.assert_not_called()
        mock_note_repo.save.assert_called_once()

    def test_create_with_valid_category(self, mock_note_repo, mock_category_repo) -> None:
        """存在するカテゴリ ID でノート作成."""
        from app.models.note_category import NoteCategory
        mock_category_repo.get_by_id_and_user.return_value = MagicMock(spec=NoteCategory)
        note_create = NoteCreate(title="タイトル", body="本文", category_id=CATEGORY_ID)
        service = NoteService(mock_note_repo, mock_category_repo)
        result = service.create_note(note_create, TEST_USER_ID)
        assert result.category_id == CATEGORY_ID

    def test_create_with_invalid_category_raises(self, mock_note_repo, mock_category_repo) -> None:
        """存在しないカテゴリ ID で NotFoundException."""
        mock_category_repo.get_by_id_and_user.return_value = None
        note_create = NoteCreate(title="タイトル", body="本文", category_id=CATEGORY_ID)
        service = NoteService(mock_note_repo, mock_category_repo)
        with pytest.raises(NotFoundException):
            service.create_note(note_create, TEST_USER_ID)


class TestNoteServiceUpdateNote:
    """update_note テスト."""

    def test_update_title(self, mock_note_repo, mock_category_repo) -> None:
        """タイトルを更新できる."""
        note = Note(user_id=TEST_USER_ID, title="旧タイトル", body="本文")
        mock_note_repo.get_by_id_and_user.return_value = note
        service = NoteService(mock_note_repo, mock_category_repo)
        result = service.update_note(NOTE_ID, NoteUpdate(title="新タイトル"), TEST_USER_ID)
        assert result.title == "新タイトル"

    def test_update_not_found_raises(self, mock_note_repo, mock_category_repo) -> None:
        """ノートが見つからない場合 NotFoundException."""
        mock_note_repo.get_by_id_and_user.return_value = None
        service = NoteService(mock_note_repo, mock_category_repo)
        with pytest.raises(NotFoundException):
            service.update_note(NOTE_ID, NoteUpdate(title="X"), TEST_USER_ID)


class TestNoteServiceDeleteNote:
    """delete_note テスト."""

    def test_delete_existing(self, mock_note_repo, mock_category_repo) -> None:
        """ノートを削除できる."""
        note = MagicMock(spec=Note)
        mock_note_repo.get_by_id_and_user.return_value = note
        service = NoteService(mock_note_repo, mock_category_repo)
        service.delete_note(NOTE_ID, TEST_USER_ID)
        mock_note_repo.delete.assert_called_once_with(note)

    def test_delete_not_found_raises(self, mock_note_repo, mock_category_repo) -> None:
        """ノートが存在しない場合 NotFoundException."""
        mock_note_repo.get_by_id_and_user.return_value = None
        service = NoteService(mock_note_repo, mock_category_repo)
        with pytest.raises(NotFoundException):
            service.delete_note(NOTE_ID, TEST_USER_ID)
