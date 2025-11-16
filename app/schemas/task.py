"""タスク関連の Pydantic スキーマ."""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskCreate(BaseModel):
    """
    タスク作成スキーマ.

    POST /tasks リクエストで使用される。
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="タスクタイトル（必須、1-255 文字）",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="タスク詳細（オプション、0-2000 文字）",
    )
    due_date: Optional[date] = Field(
        default=None,
        description="期日（オプション、YYYY-MM-DD 形式）",
    )
    is_completed: Optional[bool] = Field(
        default=False,
        description="完了状態（デフォルト: False）",
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """タイトルのバリデーション."""
        if not v or not v.strip():
            raise ValueError("タイトルは空にできません")
        if len(v) > 255:
            raise ValueError("タイトルは 255 文字以内である必要があります")
        return v.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """詳細のバリデーション."""
        if v is not None:
            if len(v) > 2000:
                raise ValueError("詳細は 2000 文字以内である必要があります")
            return v.strip() if v.strip() else None
        return v


class TaskUpdate(BaseModel):
    """
    タスク更新スキーマ.

    PUT /tasks/{task_id} リクエストで使用される。
    すべてのフィールドがオプション（部分更新対応）。
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="タスクタイトル（オプション、1-255 文字）",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="タスク詳細（オプション、0-2000 文字）",
    )
    is_completed: Optional[bool] = Field(
        default=None,
        description="完了状態（オプション）",
    )
    due_date: Optional[date] = Field(
        default=None,
        description="期日（オプション、YYYY-MM-DD 形式）",
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """タイトルのバリデーション."""
        if v is not None:
            if not v or not v.strip():
                raise ValueError("タイトルは空にできません")
            if len(v) > 255:
                raise ValueError("タイトルは 255 文字以内である必要があります")
            return v.strip()
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """詳細のバリデーション."""
        if v is not None:
            if len(v) > 2000:
                raise ValueError("詳細は 2000 文字以内である必要があります")
            return v.strip() if v.strip() else None
        return v


class TaskResponse(BaseModel):
    """
    タスクレスポンススキーマ.

    GET /tasks, POST /tasks, PUT /tasks/{task_id} のレスポンスで使用される。
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(description="タスク ID（UUID）")
    user_id: UUID = Field(description="所有者ユーザー ID（UUID）")
    title: str = Field(description="タスクタイトル")
    description: Optional[str] = Field(description="タスク詳細")
    is_completed: bool = Field(description="完了状態（True=完了、False=未完了）")
    completed_at: Optional[datetime] = Field(
        description="完了日時（ISO 8601 形式、JST）"
    )
    due_date: Optional[date] = Field(description="期日（YYYY-MM-DD 形式）")
    order: int = Field(description="表示順序")
    created_at: datetime = Field(description="作成日時（ISO 8601 形式、JST）")
    updated_at: datetime = Field(description="更新日時（ISO 8601 形式、JST）")
