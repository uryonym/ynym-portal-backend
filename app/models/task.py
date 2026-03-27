"""タスクモデル."""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Boolean, Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDPKMixin


class Task(UUIDPKMixin, TimestampMixin, Base):
    """タスクモデル."""

    __tablename__ = "task"

    user_id: Mapped[UUID] = mapped_column(index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(2000))
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    due_date: Mapped[Optional[date]] = mapped_column(Date, index=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), index=True
    )
