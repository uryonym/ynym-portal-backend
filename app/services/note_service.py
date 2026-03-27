"""ノート管理サービス."""

from typing import List
from uuid import UUID

from app.models.note import Note
from app.repositories.note_category_repository import NoteCategoryRepository
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate
from app.utils.exceptions import NotFoundException


class NoteService:
    """ノート管理ビジネスロジック層."""

    def __init__(self, note_repo: NoteRepository, category_repo: NoteCategoryRepository) -> None:
        self.note_repo = note_repo
        self.category_repo = category_repo

    def list_notes(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Note]:
        """ノート一覧を取得（カテゴリ名・タイトル昇順、カテゴリなしは末尾）."""
        return self.note_repo.list_by_user(user_id, skip, limit)

    def get_note(self, note_id: UUID, user_id: UUID) -> Note:
        """ノートを取得.

        Raises:
            NotFoundException: ノートが存在しない場合
        """
        note = self.note_repo.get_by_id_and_user(note_id, user_id)
        if not note:
            raise NotFoundException(f"ノート ID {note_id} が見つかりません")
        return note

    def _validate_category(self, category_id: UUID, user_id: UUID) -> None:
        """カテゴリがユーザーに属して存在することを検証."""
        category = self.category_repo.get_by_id_and_user(category_id, user_id)
        if not category:
            raise NotFoundException(f"カテゴリ ID {category_id} が見つかりません")

    def create_note(self, note_create: NoteCreate, user_id: UUID) -> Note:
        """ノートを作成."""
        if note_create.category_id is not None:
            self._validate_category(note_create.category_id, user_id)
        note = Note(
            user_id=user_id,
            title=note_create.title,
            body=note_create.body,
            category_id=note_create.category_id,
        )
        return self.note_repo.save(note)

    def update_note(self, note_id: UUID, note_update: NoteUpdate, user_id: UUID) -> Note:
        """ノートを部分更新."""
        note = self.get_note(note_id, user_id)
        update_data = note_update.model_dump(exclude_unset=True)
        if "category_id" in update_data and update_data["category_id"] is not None:
            self._validate_category(update_data["category_id"], user_id)
        for field, value in update_data.items():
            setattr(note, field, value)
        return self.note_repo.save(note)

    def delete_note(self, note_id: UUID, user_id: UUID) -> None:
        """ノートを物理削除."""
        note = self.get_note(note_id, user_id)
        self.note_repo.delete(note)
