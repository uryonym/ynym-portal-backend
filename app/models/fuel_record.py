"""FuelRecord（燃費記録）モデル."""

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime
from sqlmodel import Field

from app.models.base import UUIDModel

# 日本標準時 (JST)
JST = timezone(timedelta(hours=9))


class FuelRecord(UUIDModel, table=True):
    """ユーザーが記録する燃費情報.

    Attributes:
        id: 燃費記録 ID（UUID、主キー）
        vehicle_id: 車 ID（UUID、外部キー）
        user_id: ユーザー ID（UUID、外部キー）
        refuel_datetime: 給油日時（必須）
        total_mileage: 総走行距離（km、必須）
        fuel_type: 燃料タイプ（必須、例: "ハイオク", "レギュラー", "軽油"）
        unit_price: 単価（円/L、必須）
        total_cost: 総費用（円、必須）
        is_full_tank: 満タンかどうか（フラグ）
        gas_station_name: ガソリンスタンド名（例: "ENEOS 東京駅前"）
        created_at: 作成日時（JST、自動セット）
        updated_at: 更新日時（JST、自動セット）
        deleted_at: 削除日時（論理削除用）
    """

    __tablename__ = "fuel_record"

    # Foreign Keys
    vehicle_id: UUID = Field(
        index=True,
        description="車 ID（UUID、外部キー）",
    )
    user_id: UUID = Field(
        index=True,
        description="ユーザー ID（UUID、外部キー）",
    )

    # Core Fields
    refuel_datetime: datetime = Field(
        sa_type=DateTime(timezone=True),
        description="給油日時（必須）",
    )
    total_mileage: int = Field(
        gt=0,
        description="総走行距離（km、必須、正の数）",
    )
    fuel_type: str = Field(
        max_length=50,
        description="燃料タイプ（必須、例: 'ハイオク', 'レギュラー', '軽油'）",
    )
    unit_price: int = Field(
        gt=0,
        description="単価（円/L、必須、正の数）",
    )
    total_cost: int = Field(
        ge=0,
        description="総費用（円、必須、0以上の数）",
    )

    # Status Fields
    is_full_tank: bool = Field(
        default=False,
        description="満タンかどうか（フラグ）",
    )
    gas_station_name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="ガソリンスタンド名（例: 'ENEOS 東京駅前'）",
    )

    # Soft Delete Support
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        description="削除日時（論理削除用）",
    )
