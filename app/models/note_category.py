"""ノートカテゴリモデル."""

from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDPKMixin


class NoteCategory(UUIDPKMixin, TimestampMixin, Base):
    """ノートカテゴリモデル."""

    __tablename__ = "note_categories"

    user_id: Mapped[UUID] = mapped_column(index=True)
    name: Mapped[str] = mapped_column(String(255))
