"""データベースモデルのベース設定."""

from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional


class TimestampModel(SQLModel):
    """タイムスタンプフィールドを持つベースモデル."""

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
