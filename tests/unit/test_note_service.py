"""NoteService のユニットテスト."""

from unittest.mock import MagicMock
from uuid import UUID

import pytest

from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate
from app.services.note_service import NoteService
from app.utils.exceptions import NotFoundException

TEST_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")


def create_mock_result(data: list) -> MagicMock:
    """SQLAlchemy 結果オブジェクトをモック."""
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = data

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    return mock_result


class TestNoteServiceListNotes:
    """NoteService.list_notes のテストケース."""

    @pytest.fixture
    def mock_db_session(self) -> MagicMock:
        """モック DB セッション."""
        return MagicMock()

    def test_list_notes_empty(self, mock_db_session: MagicMock) -> None:
        """ノートが存在しない場合、空リストを返す."""
        mock_db_session.execute = MagicMock(return_value=create_mock_result([]))

        service = NoteService(mock_db_session)
        notes = service.list_notes(TEST_USER_ID)

        assert notes == []
        mock_db_session.execute.assert_called_once()

    def test_list_notes_with_multiple_notes(
        self, mock_db_session: MagicMock
    ) -> None:
        """複数ノートが存在する場合、ノートリストを返す."""
        note1 = MagicMock(spec=Note)
        note1.title = "ノート1"

        note2 = MagicMock(spec=Note)
        note2.title = "ノート2"

        mock_db_session.execute = MagicMock(
            return_value=create_mock_result([note1, note2])
        )

        service = NoteService(mock_db_session)
        notes = service.list_notes(TEST_USER_ID)

        assert len(notes) == 2
        assert notes[0].title == "ノート1"
        assert notes[1].title == "ノート2"


class TestNoteServiceGetNote:
    """NoteService.get_note のテストケース."""

    @pytest.fixture
    def mock_db_session(self) -> MagicMock:
        return MagicMock()

    def test_get_note_success(self, mock_db_session: MagicMock) -> None:
        """ノート取得成功."""
        note_id = UUID("11111111-1111-1111-1111-111111111111")
        note = MagicMock(spec=Note)
        note.id = note_id

        mock_result = MagicMock()
        mock_result.scalars().one_or_none.return_value = note
        mock_db_session.execute.return_value = mock_result

        service = NoteService(mock_db_session)
        result = service.get_note(note_id, TEST_USER_ID)

        assert result.id == note_id

    def test_get_note_not_found(self, mock_db_session: MagicMock) -> None:
        """ノートが見つからない場合は例外."""
        note_id = UUID("22222222-2222-2222-2222-222222222222")

        mock_result = MagicMock()
        mock_result.scalars().one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result

        service = NoteService(mock_db_session)
        with pytest.raises(NotFoundException):
            service.get_note(note_id, TEST_USER_ID)


class TestNoteServiceCreateNote:
    """NoteService.create_note のテストケース."""

    @pytest.fixture
    def mock_db_session(self) -> MagicMock:
        return MagicMock()

    def test_create_note_success(self, mock_db_session: MagicMock) -> None:
        """ノート作成成功."""
        note_create = NoteCreate(title="タイトル", body="本文")

        mock_db_session.add = MagicMock()
        mock_db_session.commit = MagicMock()
        mock_db_session.refresh = MagicMock()

        service = NoteService(mock_db_session)
        result = service.create_note(note_create, TEST_USER_ID)

        assert result.user_id == TEST_USER_ID
        assert result.title == "タイトル"
        assert result.body == "本文"
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()

    def test_create_note_with_invalid_category_fails(
        self, mock_db_session: MagicMock
    ) -> None:
        """存在しないカテゴリを指定した場合は例外."""
        invalid_category_id = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
        note_create = NoteCreate(
            title="タイトル",
            body="本文",
            category_id=invalid_category_id,
        )

        mock_result = MagicMock()
        mock_result.scalars().one_or_none.return_value = None
        mock_db_session.execute = MagicMock(return_value=mock_result)
        mock_db_session.add = MagicMock()
        mock_db_session.commit = MagicMock()

        service = NoteService(mock_db_session)

        with pytest.raises(NotFoundException):
            service.create_note(note_create, TEST_USER_ID)

        mock_db_session.add.assert_not_called()
        mock_db_session.commit.assert_not_called()


class TestNoteServiceUpdateNote:
    """NoteService.update_note のテストケース."""

    @pytest.fixture
    def mock_db_session(self) -> MagicMock:
        return MagicMock()

    def test_update_note_success(self, mock_db_session: MagicMock) -> None:
        """ノート更新成功."""
        note_id = UUID("33333333-3333-3333-3333-333333333333")
        note = MagicMock(spec=Note)
        note.id = note_id
        note.title = "旧タイトル"
        note.body = "旧本文"

        service = NoteService(mock_db_session)
        service.get_note = MagicMock(return_value=note)
        mock_db_session.commit = MagicMock()
        mock_db_session.refresh = MagicMock()

        note_update = NoteUpdate(title="新タイトル")
        updated = service.update_note(note_id, note_update, TEST_USER_ID)

        assert updated.title == "新タイトル"
        assert updated.body == "旧本文"

    def test_update_note_with_invalid_category_fails(
        self, mock_db_session: MagicMock
    ) -> None:
        """存在しないカテゴリを指定した更新は例外."""
        note_id = UUID("55555555-5555-5555-5555-555555555555")
        invalid_category_id = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")

        note = MagicMock(spec=Note)
        note.id = note_id

        mock_result = MagicMock()
        mock_result.scalars().one_or_none.return_value = None
        mock_db_session.execute = MagicMock(return_value=mock_result)
        mock_db_session.commit = MagicMock()

        service = NoteService(mock_db_session)
        service.get_note = MagicMock(return_value=note)

        note_update = NoteUpdate(category_id=invalid_category_id)

        with pytest.raises(NotFoundException):
            service.update_note(note_id, note_update, TEST_USER_ID)

        mock_db_session.commit.assert_not_called()


class TestNoteServiceDeleteNote:
    """NoteService.delete_note のテストケース."""

    @pytest.fixture
    def mock_db_session(self) -> MagicMock:
        return MagicMock()

    def test_delete_note_success(self, mock_db_session: MagicMock) -> None:
        """ノート削除成功."""
        note_id = UUID("44444444-4444-4444-4444-444444444444")
        note = MagicMock(spec=Note)
        note.id = note_id

        service = NoteService(mock_db_session)
        service.get_note = MagicMock(return_value=note)
        mock_db_session.delete = MagicMock()
        mock_db_session.commit = MagicMock()

        service.delete_note(note_id, TEST_USER_ID)

        mock_db_session.delete.assert_called_once_with(note)
        mock_db_session.commit.assert_called_once()
