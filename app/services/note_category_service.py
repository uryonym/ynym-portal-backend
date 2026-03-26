"""ノートカテゴリ管理サービス."""

from typing import List
from uuid import UUID

from sqlalchemy import asc, select, update
from sqlalchemy.orm import Session
from sqlmodel import col

from app.models.note import Note
from app.models.note_category import NoteCategory
from app.schemas.note_category import NoteCategoryCreate, NoteCategoryUpdate
from app.utils.exceptions import NotFoundException


class NoteCategoryService:
    """ノートカテゴリ管理ビジネスロジック層."""

    def __init__(self, db_session: Session) -> None:
        """初期化.

        Args:
            db_session: データベースセッション
        """
        self.db_session = db_session

    def list_categories(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[NoteCategory]:
        """カテゴリ一覧を取得."""
        stmt = (
            select(NoteCategory)
            .where(col(NoteCategory.user_id) == user_id)
            .order_by(asc(col(NoteCategory.name)))
            .offset(skip)
            .limit(limit)
        )
        result = self.db_session.execute(stmt)
        return list(result.scalars().all())

    def get_category(self, category_id: UUID, user_id: UUID) -> NoteCategory:
        """カテゴリを取得.

        Raises:
            NotFoundException: カテゴリが見つからない場合
        """
        stmt = (
            select(NoteCategory)
            .where(col(NoteCategory.id) == category_id)
            .where(col(NoteCategory.user_id) == user_id)
        )
        result = self.db_session.execute(stmt)
        category = result.scalars().one_or_none()
        if not category:
            raise NotFoundException(f"カテゴリ ID {category_id} が見つかりません")
        return category

    def create_category(
        self, category_create: NoteCategoryCreate, user_id: UUID
    ) -> NoteCategory:
        """カテゴリを作成."""
        category = NoteCategory(user_id=user_id, name=category_create.name)
        self.db_session.add(category)
        self.db_session.commit()
        self.db_session.refresh(category)
        return category

    def update_category(
        self,
        category_id: UUID,
        category_update: NoteCategoryUpdate,
        user_id: UUID,
    ) -> NoteCategory:
        """カテゴリを更新（部分更新）."""
        category = self.get_category(category_id, user_id)
        update_data = category_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        self.db_session.add(category)
        self.db_session.commit()
        self.db_session.refresh(category)
        return category

    def delete_category(self, category_id: UUID, user_id: UUID) -> None:
        """カテゴリを削除し、関連ノートを未分類にする."""
        category = self.get_category(category_id, user_id)

        stmt = (
            update(Note)
            .where(col(Note.user_id) == user_id)
            .where(col(Note.category_id) == category_id)
            .values(category_id=None)
        )
        self.db_session.execute(stmt)
        self.db_session.delete(category)
        self.db_session.commit()
