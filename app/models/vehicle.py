"""Vehicle（車）モデル."""

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel

# 日本標準時 (JST)
JST = timezone(timedelta(hours=9))


class Vehicle(SQLModel, table=True):
    """ユーザーが所有する車情報.

    Attributes:
        id: 車 ID（UUID、主キー）
        user_id: ユーザー ID（UUID、外部キー）
        name: 車名（必須、1-255 文字）
        seq: シーケンス（車の登録順番、数値型）
        maker: メーカー（必須、1-100 文字）
        model: 型式（必須、1-100 文字）
        year: 年式（例: 2023）
        number: ナンバー（例: "東京 123あ 1234"、1-50 文字）
        tank_capacity: タンク容量（L、例: 50.0）
        created_at: 作成日時（JST、自動セット）
        updated_at: 更新日時（JST、自動セット）
        deleted_at: 削除日時（論理削除用）
    """

    __tablename__ = "vehicle"

    id: UUID = Field(default_factory=lambda: __import__("uuid").uuid4(), primary_key=True)
    user_id: UUID
    name: str = Field(max_length=255)
    seq: int
    maker: str = Field(max_length=100)
    model: str = Field(max_length=100)
    year: Optional[int] = None
    number: Optional[str] = Field(default=None, max_length=50)
    tank_capacity: Optional[float] = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(JST),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(JST),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),
    )
