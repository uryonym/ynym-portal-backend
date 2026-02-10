"""ノート関連の Pydantic スキーマ."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class NoteCreate(BaseModel):
    """ノート作成スキーマ."""

    title: str = Field(
        ..., min_length=1, max_length=255, description="タイトル（必須、1-255 文字）"
    )
    body: str = Field(..., description="本文（必須）")
    category_id: Optional[UUID] = Field(default=None, description="カテゴリ ID（任意）")

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """タイトルのバリデーション."""
        if not v or not v.strip():
            raise ValueError("タイトルは必須項目です")
        if len(v) > 255:
            raise ValueError("タイトルは 255 文字以内である必要があります")
        return v.strip()

    @field_validator("body")
    @classmethod
    def validate_body(cls, v: str) -> str:
        """本文のバリデーション."""
        if not v or not v.strip():
            raise ValueError("本文は必須項目です")
        return v.strip()


class NoteUpdate(BaseModel):
    """ノート更新スキーマ."""

    title: Optional[str] = Field(
        default=None, min_length=1, max_length=255, description="タイトル（オプション）"
    )
    body: Optional[str] = Field(default=None, description="本文（オプション）")
    category_id: Optional[UUID] = Field(default=None, description="カテゴリ ID（任意）")

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """タイトルのバリデーション."""
        if v is not None:
            if not v.strip():
                raise ValueError("タイトルは空にできません")
            if len(v) > 255:
                raise ValueError("タイトルは 255 文字以内である必要があります")
            return v.strip()
        return v

    @field_validator("body")
    @classmethod
    def validate_body(cls, v: Optional[str]) -> Optional[str]:
        """本文のバリデーション."""
        if v is not None:
            if not v.strip():
                raise ValueError("本文は空にできません")
            return v.strip()
        return v


class NoteResponse(BaseModel):
    """ノートレスポンススキーマ."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(description="ノート ID（UUID）")
    user_id: UUID = Field(description="所有者ユーザー ID（UUID）")
    category_id: Optional[UUID] = Field(description="カテゴリ ID（任意）")
    title: str = Field(description="タイトル")
    body: str = Field(description="本文")
    created_at: datetime = Field(description="作成日時（JST）")
    updated_at: datetime = Field(description="更新日時（JST）")
