"""燃費記録モデル."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime
from sqlmodel import Field

from app.models.base import UUIDModel


class FuelRecord(UUIDModel, table=True):
    """
    燃費記録モデル.

    ユーザーが記録・管理する給油・燃費情報を表現する。

    Attributes:
        vehicle_id: 対象車両の UUID（将来 FK 制約追加予定）
        user_id: 記録ユーザーの UUID（将来 FK 制約追加予定）
        refuel_datetime: 給油日時（必須、日本時間 JST）
        total_mileage: 総走行距離（必須、km 単位、正の整数）
        fuel_type: 燃料タイプ（必須、50 字以内、例: "ハイオク", "レギュラー", "軽油"）
        unit_price: 燃料単価（必須、円/L 単位、正の整数）
        total_cost: 総費用（必須、円単位、0 以上の整数）
        is_full_tank: 満タン給油フラグ（True=満タン、False=一部給油）
        gas_station_name: ガソリンスタンド名（オプション、255 字以内）
        deleted_at: 論理削除日時（初期バージョンは未使用、将来対応）
    """

    __tablename__ = "fuel_record"

    # Foreign Keys
    vehicle_id: UUID = Field(
        index=True,
        description="対象車両の UUID（将来 FK 制約追加予定）",
    )
    user_id: UUID = Field(
        index=True,
        description="記録ユーザーの UUID（将来 FK 制約追加予定）",
    )

    # Core Fields
    refuel_datetime: datetime = Field(
        sa_type=DateTime(timezone=True),
        description="給油日時（必須、日本時間 JST）",
    )
    total_mileage: int = Field(
        gt=0,
        description="総走行距離（必須、km 単位、正の整数）",
    )
    fuel_type: str = Field(
        max_length=50,
        description="燃料タイプ（必須、50 字以内、例: 'ハイオク', 'レギュラー', '軽油'）",
    )
    unit_price: int = Field(
        gt=0,
        description="燃料単価（必須、円/L 単位、正の整数）",
    )
    total_cost: int = Field(
        ge=0,
        description="総費用（必須、円単位、0 以上の整数）",
    )

    # Status Fields
    is_full_tank: bool = Field(
        default=False,
        description="満タン給油フラグ（True=満タン、False=一部給油）",
    )
    gas_station_name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="ガソリンスタンド名（オプション、255 字以内、例: 'ENEOS 東京駅前'）",
    )

    # Soft Delete Support (Future)
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        index=True,
        description="論理削除日時（日本時間 JST、初期バージョンは未使用、将来対応）",
    )
