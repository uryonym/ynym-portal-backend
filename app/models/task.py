"""タスクモデル."""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field

from app.models.base import UUIDModel


class Task(UUIDModel, table=True):
    """
    タスクモデル.

    ユーザーが作成・管理するタスクを表現する。

    Attributes:
        user_id: タスク所有ユーザーの UUID（将来 FK 制約追加予定）
        title: タスクのタイトル（必須、255 字以内）
        description: タスクの詳細説明（オプション、2000 字以内）
        is_completed: 完了状態フラグ（True=完了、False=未完了）
        completed_at: タスク完了日時（日本時間 JST）
        due_date: タスク期日（オプション、YYYY-MM-DD 形式）
        order: ドラッグ&ドロップ用表示順序（将来の UI ソート対応）
        deleted_at: 論理削除日時（初期バージョンは未使用、将来対応）
    """

    __tablename__ = "task"

    # Foreign Keys
    user_id: UUID = Field(
        index=True,
        description="タスク所有ユーザーの UUID（将来 FK 制約追加予定）",
    )

    # Core Fields
    title: str = Field(
        max_length=255,
        index=False,
        description="タスクのタイトル（必須、255 字以内）",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="タスクの詳細説明（オプション、2000 字以内）",
    )

    # Status Fields
    is_completed: bool = Field(
        default=False,
        description="完了状態フラグ（True=完了、False=未完了）",
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        description="タスク完了日時（日本時間 JST）",
    )

    # Deadline
    due_date: Optional[date] = Field(
        default=None,
        index=True,
        description="タスク期日（オプション、YYYY-MM-DD 形式）",
    )

    # Ordering
    order: int = Field(
        default=0,
        ge=0,
        description="ドラッグ&ドロップ用表示順序（将来の UI ソート対応）",
    )

    # Soft Delete Support (Future)
    deleted_at: Optional[datetime] = Field(
        default=None,
        index=True,
        description="論理削除日時（初期バージョンは未使用、将来対応）",
    )
