"""ノートカテゴリモデル."""

from uuid import UUID

from sqlmodel import Field

from app.models.base import UUIDModel


class NoteCategory(UUIDModel, table=True):
    """
    ノートカテゴリモデル.

    ユーザーが作成するノートのカテゴリを表現する。

    Attributes:
        user_id: カテゴリ所有ユーザーの UUID
        name: カテゴリ名（必須、255 字以内）
    """

    __tablename__ = "note_categories"

    # Foreign Keys
    user_id: UUID = Field(
        index=True,
        description="カテゴリ所有ユーザーの UUID",
    )

    # Core Fields
    name: str = Field(
        max_length=255,
        description="カテゴリ名（必須、255 字以内）",
    )
