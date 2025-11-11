"""データベースモデルのベース設定."""

from datetime import UTC, datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

# 日本時間（JST）のタイムゾーン設定
JST = timezone(timedelta(hours=9))


class TimestampModel(SQLModel):
    """
    作成日時・更新日時フィールドを持つ基本モデル.

    すべてのドメインモデルはこのクラスを継承する.
    """

    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(JST),
        nullable=False,
        description="レコード作成日時（日本時間 JST）",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(JST),
        nullable=False,
        description="レコード最終更新日時（日本時間 JST）",
    )


class UUIDModel(TimestampModel):
    """
    UUID プライマリキーを持つ基本モデル.

    すべてのドメインモデルはこのクラスを継承し、
    UUID ベースのグローバルユニークな ID を自動生成される.

    利点：
    - グローバルユニーク：全世界でユニークな ID 生成
    - 分散環境対応：DB レプリケーション・マイクロサービス対応
    - プライバシー保護：シーケンシャル ID と異なり予測不可能
    """

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        description="UUID プライマリキー（RFC 4122 準拠）",
    )
