"""車両モデル."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime
from sqlmodel import Field

from app.models.base import UUIDModel


class Vehicle(UUIDModel, table=True):
    """
    車両モデル.

    ユーザーが所有・管理する車両情報を表現する。

    Attributes:
        user_id: 車両所有ユーザーの UUID（将来 FK 制約追加予定）
        name: 車両名（必須、255 字以内）
        seq: 表示順序（ユーザー内での登録順番、0 以上の整数）
        maker: メーカー名（必須、100 字以内）
        model: 型式・モデル名（必須、100 字以内）
        year: 年式（オプション、例: 2023）
        number: ナンバープレート（オプション、50 字以内、例: "東京 123あ 1234"）
        tank_capacity: 燃料タンク容量（オプション、リットル単位、例: 50.0）
        deleted_at: 論理削除日時（初期バージョンは未使用、将来対応）
    """

    __tablename__ = "vehicle"

    # Foreign Keys
    user_id: UUID = Field(
        index=True,
        description="車両所有ユーザーの UUID（将来 FK 制約追加予定）",
    )

    # Core Fields
    name: str = Field(
        max_length=255,
        description="車両名（必須、255 字以内）",
    )
    seq: int = Field(
        ge=0,
        description="表示順序（ユーザー内での登録順番、0 以上の整数）",
    )
    maker: str = Field(
        max_length=100,
        description="メーカー名（必須、100 字以内）",
    )
    model: str = Field(
        max_length=100,
        description="型式・モデル名（必須、100 字以内）",
    )

    # Optional Fields
    year: Optional[int] = Field(
        default=None,
        description="年式（オプション、例: 2023）",
    )
    number: Optional[str] = Field(
        default=None,
        max_length=50,
        description="ナンバープレート（オプション、50 字以内、例: '東京 123あ 1234'）",
    )
    tank_capacity: Optional[float] = Field(
        default=None,
        gt=0,
        description="燃料タンク容量（オプション、リットル単位、例: 50.0）",
    )

    # Soft Delete Support (Future)
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        index=True,
        description="論理削除日時（日本時間 JST、初期バージョンは未使用、将来対応）",
    )
