"""ノート管理サービス."""

from typing import List
from uuid import UUID

from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import nulls_last
from sqlmodel import col

from app.models.note import Note
from app.models.note_category import NoteCategory
from app.schemas.note import NoteCreate, NoteUpdate
from app.utils.exceptions import NotFoundException


class NoteService:
    """ノート管理ビジネスロジック層."""

    def __init__(self, db_session: AsyncSession) -> None:
        """初期化.

        Args:
            db_session: データベースセッション
        """
        self.db_session = db_session

    async def list_notes(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Note]:
        """ノート一覧を取得.

        既定の並び順はカテゴリ名、次にタイトルの昇順。
        カテゴリ未設定は末尾に配置する。
        """
        stmt = (
            select(Note)
            .outerjoin(NoteCategory, Note.category_id == NoteCategory.id)
            .where(col(Note.user_id) == user_id)
            .order_by(
                nulls_last(asc(col(NoteCategory.name))),
                asc(col(Note.title)),
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_note(self, note_id: UUID, user_id: UUID) -> Note:
        """ノートを取得.

        Raises:
            NotFoundException: ノートが見つからない場合
        """
        stmt = (
            select(Note)
            .where(col(Note.id) == note_id)
            .where(col(Note.user_id) == user_id)
        )
        result = await self.db_session.execute(stmt)
        note = result.scalars().one_or_none()
        if not note:
            raise NotFoundException(f"ノート ID {note_id} が見つかりません")
        return note

    async def create_note(self, note_create: NoteCreate, user_id: UUID) -> Note:
        """ノートを作成."""
        note = Note(
            user_id=user_id,
            title=note_create.title,
            body=note_create.body,
            category_id=note_create.category_id,
        )
        self.db_session.add(note)
        await self.db_session.commit()
        await self.db_session.refresh(note)
        return note

    async def update_note(
        self,
        note_id: UUID,
        note_update: NoteUpdate,
        user_id: UUID,
    ) -> Note:
        """ノートを更新（部分更新）."""
        note = await self.get_note(note_id, user_id)
        update_data = note_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(note, field, value)
        self.db_session.add(note)
        await self.db_session.commit()
        await self.db_session.refresh(note)
        return note

    async def delete_note(self, note_id: UUID, user_id: UUID) -> None:
        """ノートを削除（物理削除）."""
        note = await self.get_note(note_id, user_id)
        await self.db_session.delete(note)
        await self.db_session.commit()
