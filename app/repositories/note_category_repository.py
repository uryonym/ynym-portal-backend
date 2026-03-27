"""ノートカテゴリリポジトリ."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import asc, select

from app.models.note_category import NoteCategory
from app.repositories.base import BaseRepository


class NoteCategoryRepository(BaseRepository[NoteCategory]):
    """ノートカテゴリに関するデータアクセスを担う."""

    def __init__(self, session) -> None:
        super().__init__(session, NoteCategory)

    def list_by_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[NoteCategory]:
        """ユーザーのカテゴリ一覧を名前昇順で取得."""
        stmt = (
            select(NoteCategory)
            .where(NoteCategory.user_id == user_id)
            .order_by(asc(NoteCategory.name))
            .offset(skip)
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_by_id_and_user(
        self, category_id: UUID, user_id: UUID
    ) -> Optional[NoteCategory]:
        """category_id と user_id でカテゴリを取得（所有権確認）."""
        stmt = (
            select(NoteCategory)
            .where(NoteCategory.id == category_id)
            .where(NoteCategory.user_id == user_id)
        )
        return self.session.execute(stmt).scalars().one_or_none()
