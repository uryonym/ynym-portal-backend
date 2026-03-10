"""ノートモデル."""

from typing import Optional
from uuid import UUID

from sqlmodel import Field

from app.models.base import UUIDModel


class Note(UUIDModel, table=True):
    """
    ノートモデル.

    ユーザーが作成・管理するノートを表現する。

    Attributes:
        user_id: ノート所有ユーザーの UUID
        category_id: カテゴリ ID（任意）
        title: タイトル（必須、255 字以内）
        body: 本文（必須）
    """

    __tablename__ = "notes"

    # Foreign Keys
    user_id: UUID = Field(
        index=True,
        description="ノート所有ユーザーの UUID",
    )
    category_id: Optional[UUID] = Field(
        default=None,
        index=True,
        description="カテゴリ ID（任意）",
    )

    # Core Fields
    title: str = Field(
        max_length=255,
        description="タイトル（必須、255 字以内）",
    )
    body: str = Field(
        description="本文（必須）",
    )
