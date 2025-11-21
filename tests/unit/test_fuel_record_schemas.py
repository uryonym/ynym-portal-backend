"""FuelRecord（燃費記録）スキーマバリデーションテスト."""

import pytest
from datetime import datetime, timedelta, timezone
from pydantic import ValidationError
from uuid import UUID

from app.schemas.fuel_record import FuelRecordCreate, FuelRecordUpdate

JST = timezone(timedelta(hours=9))


class TestFuelRecordCreateSchema:
    """FuelRecordCreate スキーマバリデーション."""

    def test_fuel_record_create_valid_with_all_fields(self) -> None:
        """すべてのフィールド指定で有効."""
        vehicle_id = UUID("550e8400-e29b-41d4-a716-446655440001")
        now = datetime.now(JST)

        schema = FuelRecordCreate(
            vehicle_id=vehicle_id,
            refuel_datetime=now,
            total_mileage=100,
            fuel_type="ハイオク",
            unit_price=165,
            total_cost=6600,
            is_full_tank=True,
            gas_station_name="ENEOS 東京駅前",
        )

        assert schema.vehicle_id == vehicle_id
        assert schema.refuel_datetime == now
        assert schema.total_mileage == 100
        assert schema.fuel_type == "ハイオク"
        assert schema.unit_price == 165
        assert schema.total_cost == 6600
        assert schema.is_full_tank is True
        assert schema.gas_station_name == "ENEOS 東京駅前"

    def test_fuel_record_create_valid_with_minimal_fields(self) -> None:
        """最小限のフィールドで有効."""
        vehicle_id = UUID("550e8400-e29b-41d4-a716-446655440001")
        now = datetime.now(JST)

        schema = FuelRecordCreate(
            vehicle_id=vehicle_id,
            refuel_datetime=now,
            total_mileage=100,
            fuel_type="ハイオク",
            unit_price=165,
            total_cost=6600,
        )

        assert schema.vehicle_id == vehicle_id
        assert schema.refuel_datetime == now
        assert schema.total_mileage == 100
        assert schema.fuel_type == "ハイオク"
        assert schema.unit_price == 165
        assert schema.total_cost == 6600
        assert schema.is_full_tank is False  # デフォルト値
        assert schema.gas_station_name is None

    def test_fuel_record_create_vehicle_id_required(self) -> None:
        """車 ID は必須."""
        now = datetime.now(JST)

        with pytest.raises(ValidationError):
            FuelRecordCreate(
                refuel_datetime=now,
                total_mileage=100,
                fuel_type="ハイオク",
                unit_price=165,
                total_cost=6600,
            )

    def test_fuel_record_create_total_mileage_positive(self) -> None:
        """走行距離は正の数."""
        vehicle_id = UUID("550e8400-e29b-41d4-a716-446655440001")
        now = datetime.now(JST)

        with pytest.raises(ValidationError) as exc_info:
            FuelRecordCreate(
                vehicle_id=vehicle_id,
                refuel_datetime=now,
                total_mileage=-50,
                fuel_type="ハイオク",
                unit_price=165,
                total_cost=6600,
            )
        assert "greater than 0" in str(exc_info.value).lower()

    def test_fuel_record_create_unit_price_positive(self) -> None:
        """単価は正の数."""
        vehicle_id = UUID("550e8400-e29b-41d4-a716-446655440001")
        now = datetime.now(JST)

        with pytest.raises(ValidationError) as exc_info:
            FuelRecordCreate(
                vehicle_id=vehicle_id,
                refuel_datetime=now,
                total_mileage=100,
                fuel_type="ハイオク",
                unit_price=-165,
                total_cost=6600,
            )
        assert "greater than 0" in str(exc_info.value).lower()

    def test_fuel_record_create_total_cost_non_negative(self) -> None:
        """総費用は 0 以上の数."""
        vehicle_id = UUID("550e8400-e29b-41d4-a716-446655440001")
        now = datetime.now(JST)

        with pytest.raises(ValidationError) as exc_info:
            FuelRecordCreate(
                vehicle_id=vehicle_id,
                refuel_datetime=now,
                total_mileage=100,
                fuel_type="ハイオク",
                unit_price=165,
                total_cost=-100,
            )
        assert "greater than or equal to 0" in str(exc_info.value).lower()

    def test_fuel_record_create_fuel_type_required(self) -> None:
        """燃料タイプは必須."""
        vehicle_id = UUID("550e8400-e29b-41d4-a716-446655440001")
        now = datetime.now(JST)

        with pytest.raises(ValidationError):
            FuelRecordCreate(
                vehicle_id=vehicle_id,
                refuel_datetime=now,
                total_mileage=100,
                fuel_type="",
                unit_price=165,
                total_cost=6600,
            )

    def test_fuel_record_create_fuel_type_whitespace_trimmed(self) -> None:
        """燃料タイプの前後の空白はトリム."""
        vehicle_id = UUID("550e8400-e29b-41d4-a716-446655440001")
        now = datetime.now(JST)

        schema = FuelRecordCreate(
            vehicle_id=vehicle_id,
            refuel_datetime=now,
            total_mileage=100,
            fuel_type="  ハイオク  ",
            unit_price=165,
            total_cost=6600,
        )

        assert schema.fuel_type == "ハイオク"

    def test_fuel_record_create_gas_station_name_whitespace_trimmed(self) -> None:
        """ガソリンスタンド名の前後の空白はトリム."""
        vehicle_id = UUID("550e8400-e29b-41d4-a716-446655440001")
        now = datetime.now(JST)

        schema = FuelRecordCreate(
            vehicle_id=vehicle_id,
            refuel_datetime=now,
            total_mileage=100,
            fuel_type="ハイオク",
            unit_price=165,
            total_cost=6600,
            gas_station_name="  ENEOS 東京駅前  ",
        )

        assert schema.gas_station_name == "ENEOS 東京駅前"


class TestFuelRecordUpdateSchema:
    """FuelRecordUpdate スキーマバリデーション."""

    def test_fuel_record_update_all_fields_optional(self) -> None:
        """すべてのフィールドはオプション."""
        schema = FuelRecordUpdate()

        assert schema.refuel_datetime is None
        assert schema.total_mileage is None
        assert schema.fuel_type is None
        assert schema.unit_price is None
        assert schema.total_cost is None
        assert schema.is_full_tank is None
        assert schema.gas_station_name is None

    def test_fuel_record_update_partial_update(self) -> None:
        """特定のフィールドのみ更新可能."""
        schema = FuelRecordUpdate(fuel_type="レギュラー", is_full_tank=False)

        assert schema.fuel_type == "レギュラー"
        assert schema.is_full_tank is False
        assert schema.total_mileage is None
        assert schema.unit_price is None

    def test_fuel_record_update_total_mileage_positive(self) -> None:
        """走行距離は正の数."""
        with pytest.raises(ValidationError) as exc_info:
            FuelRecordUpdate(total_mileage=-50)
        assert "greater than 0" in str(exc_info.value).lower()

    def test_fuel_record_update_fuel_type_validation(self) -> None:
        """燃料タイプが空白のみの場合は不可."""
        with pytest.raises(ValidationError) as exc_info:
            FuelRecordUpdate(fuel_type="   ")
        assert "燃料タイプは必須項目です" in str(exc_info.value)
