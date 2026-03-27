"""ノートモデル."""

from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDPKMixin


class Note(UUIDPKMixin, TimestampMixin, Base):
    """ノートモデル."""

    __tablename__ = "notes"

    user_id: Mapped[UUID] = mapped_column(index=True)
    category_id: Mapped[Optional[UUID]] = mapped_column(index=True)
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
