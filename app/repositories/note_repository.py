"""ノートリポジトリ."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import asc, select, update
from sqlalchemy.sql import nulls_last

from app.models.note import Note
from app.models.note_category import NoteCategory
from app.repositories.base import BaseRepository


class NoteRepository(BaseRepository[Note]):
    """ノートに関するデータアクセスを担う."""

    def __init__(self, session) -> None:
        super().__init__(session, Note)

    def list_by_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Note]:
        """ユーザーのノート一覧をカテゴリ名・タイトル昇順で取得."""
        stmt = (
            select(Note)
            .outerjoin(NoteCategory, Note.category_id == NoteCategory.id)
            .where(Note.user_id == user_id)
            .order_by(
                nulls_last(asc(NoteCategory.name)),
                asc(Note.title),
            )
            .offset(skip)
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_by_id_and_user(self, note_id: UUID, user_id: UUID) -> Optional[Note]:
        """note_id と user_id でノートを取得（所有権確認）."""
        stmt = select(Note).where(Note.id == note_id).where(Note.user_id == user_id)
        return self.session.execute(stmt).scalars().one_or_none()

    def nullify_category(self, user_id: UUID, category_id: UUID) -> None:
        """指定カテゴリに属するノートのカテゴリを NULL に更新（コミットなし）."""
        stmt = (
            update(Note)
            .where(Note.user_id == user_id)
            .where(Note.category_id == category_id)
            .values(category_id=None)
        )
        self.session.execute(stmt)
