"""FuelRecord（燃費記録）Pydantic スキーマ."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class FuelRecordCreate(BaseModel):
    """燃費記録作成スキーマ.

    Attributes:
        vehicle_id: 車 ID（UUID、必須）
        refuel_datetime: 給油日時（必須）
        total_mileage: 総走行距離（km、必須、正の数）
        fuel_type: 燃料タイプ（必須、例: "ハイオク"）
        unit_price: 単価（円/L、必須、正の数）
        total_cost: 総費用（円、必須、0以上の数）
        is_full_tank: 満タンかどうか（デフォルト: False）
        gas_station_name: ガソリンスタンド名（オプション）
    """

    vehicle_id: UUID = Field(description="車 ID（UUID、必須）")
    refuel_datetime: datetime = Field(description="給油日時（必須）")
    total_mileage: int = Field(
        gt=0,
        description="総走行距離（km、必須、正の数）",
    )
    fuel_type: str = Field(
        min_length=1,
        max_length=50,
        description="燃料タイプ（例: 'ハイオク', 'レギュラー', '軽油'）",
    )
    unit_price: int = Field(
        gt=0,
        description="単価（円/L、必須、正の数）",
    )
    total_cost: int = Field(
        ge=0,
        description="総費用（円、0以上の数）",
    )
    is_full_tank: bool = Field(
        default=False,
        description="満タンかどうか",
    )
    gas_station_name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="ガソリンスタンド名",
    )

    @field_validator("fuel_type")
    @classmethod
    def validate_fuel_type(cls, v: str) -> str:
        """燃料タイプを検証."""
        v = v.strip()
        if not v:
            raise ValueError("燃料タイプは必須項目です")
        return v

    @field_validator("gas_station_name")
    @classmethod
    def validate_gas_station_name(cls, v: Optional[str]) -> Optional[str]:
        """ガソリンスタンド名を検証."""
        if v is not None:
            v = v.strip()
            if not v:
                return None
        return v


class FuelRecordUpdate(BaseModel):
    """燃費記録更新スキーマ.

    Attributes:
        refuel_datetime: 給油日時（オプション）
        total_mileage: 総走行距離（km、オプション、正の数）
        fuel_type: 燃料タイプ（オプション）
        unit_price: 単価（円/L、オプション、正の数）
        total_cost: 総費用（円、オプション、0以上の数）
        is_full_tank: 満タンかどうか（オプション）
        gas_station_name: ガソリンスタンド名（オプション）
    """

    refuel_datetime: Optional[datetime] = Field(
        default=None,
        description="給油日時",
    )
    total_mileage: Optional[int] = Field(
        default=None,
        gt=0,
        description="総走行距離（km、正の数）",
    )
    fuel_type: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="燃料タイプ",
    )
    unit_price: Optional[int] = Field(
        default=None,
        gt=0,
        description="単価（円/L、正の数）",
    )
    total_cost: Optional[int] = Field(
        default=None,
        ge=0,
        description="総費用（円、0以上の数）",
    )
    is_full_tank: Optional[bool] = Field(
        default=None,
        description="満タンかどうか",
    )
    gas_station_name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="ガソリンスタンド名",
    )

    @field_validator("fuel_type")
    @classmethod
    def validate_fuel_type(cls, v: Optional[str]) -> Optional[str]:
        """燃料タイプを検証."""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("燃料タイプは必須項目です")
        return v

    @field_validator("gas_station_name")
    @classmethod
    def validate_gas_station_name(cls, v: Optional[str]) -> Optional[str]:
        """ガソリンスタンド名を検証."""
        if v is not None:
            v = v.strip()
            if not v:
                return None
        return v


class FuelRecordResponse(BaseModel):
    """燃費記録レスポンススキーマ.

    API から返されるフォーマット.
    """

    id: UUID = Field(description="燃費記録 ID（UUID）")
    vehicle_id: UUID = Field(description="車 ID（UUID）")
    user_id: UUID = Field(description="ユーザー ID（UUID）")
    refuel_datetime: datetime = Field(description="給油日時")
    total_mileage: int = Field(description="総走行距離（km）")
    fuel_type: str = Field(description="燃料タイプ")
    unit_price: int = Field(description="単価（円/L）")
    total_cost: int = Field(description="総費用（円）")
    is_full_tank: bool = Field(description="満タンかどうか")
    gas_station_name: Optional[str] = Field(description="ガソリンスタンド名")
    distance_traveled: Optional[int] = Field(
        default=None,
        description="走行距離（km）: 今回の総走行距離 - 前回の総走行距離",
    )
    fuel_amount: Optional[float] = Field(
        default=None,
        description="給油量（L）: 総費用 / 単価",
    )
    fuel_efficiency: Optional[float] = Field(
        default=None,
        description="燃費（km/L）: 走行距離 / 給油量（小数点2桁）",
    )
    created_at: datetime = Field(description="作成日時（JST）")
    updated_at: datetime = Field(description="更新日時（JST）")

    class Config:
        """Pydantic v2 設定."""

        from_attributes = True
