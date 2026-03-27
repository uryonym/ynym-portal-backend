"""データベースモデルのベース設定."""

from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 日本時間（JST）のタイムゾーン設定
JST = timezone(timedelta(hours=9))


class Base(DeclarativeBase):
    """SQLAlchemy 宣言ベースクラス."""

    pass


class TimestampMixin:
    """作成日時・更新日時フィールドを持つ Mixin.

    Note: PostgreSQL TIMESTAMP WITH TIME ZONE に日本時間（JST）で保存されます。
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(JST),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(JST),
        onupdate=lambda: datetime.now(JST),
        nullable=False,
    )


class UUIDPKMixin:
    """UUID プライマリキーを持つ Mixin.

    UUID ベースのグローバルユニークな ID を自動生成する。
    """

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )


# 後方互換エイリアス（既存コードからの移行期）
TimestampModel = TimestampMixin
UUIDModel = UUIDPKMixin
