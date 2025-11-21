"""FuelRecord（燃費記録）サービステスト."""

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

from app.models.fuel_record import FuelRecord
from app.schemas.fuel_record import FuelRecordCreate, FuelRecordUpdate
from app.services.fuel_record_service import FuelRecordService

JST = timezone(timedelta(hours=9))


@pytest.fixture
def mock_db_session() -> AsyncMock:
    """モック DB セッション."""
    return AsyncMock()


class TestFuelRecordServiceListFuelRecords:
    """FuelRecordService.list_fuel_records テスト."""

    @pytest.mark.asyncio
    async def test_list_fuel_records_empty(self, mock_db_session: AsyncMock) -> None:
        """燃費記録がない場合."""
        user_id = UUID("550e8400-e29b-41d4-a716-446655440000")
        vehicle_id = UUID("550e8400-e29b-41d4-a716-446655440001")

        mock_result = MagicMock()
        mock_result.scalars().all.return_value = []
        mock_db_session.execute.return_value = mock_result

        service = FuelRecordService(mock_db_session)
        records = await service.list_fuel_records(user_id=user_id, vehicle_id=vehicle_id)

        assert records == []

    @pytest.mark.asyncio
    async def test_list_fuel_records_with_multiple_records(
        self, mock_db_session: AsyncMock
    ) -> None:
        """複数の燃費記録がある場合."""
        user_id = UUID("550e8400-e29b-41d4-a716-446655440000")
        vehicle_id = UUID("550e8400-e29b-41d4-a716-446655440001")
        now = datetime.now(JST)

        record1 = FuelRecord(
            id=UUID("550e8400-e29b-41d4-a716-446655440101"),
            vehicle_id=vehicle_id,
            user_id=user_id,
            refuel_datetime=now,
            total_mileage=100,
            fuel_type="ハイオク",
            unit_price=165,
            total_cost=6600,
            created_at=now,
            updated_at=now,
        )
        record2 = FuelRecord(
            id=UUID("550e8400-e29b-41d4-a716-446655440102"),
            vehicle_id=vehicle_id,
            user_id=user_id,
            refuel_datetime=now,
            total_mileage=200,
            fuel_type="レギュラー",
            unit_price=160,
            total_cost=6400,
            created_at=now,
            updated_at=now,
        )

        mock_result = MagicMock()
        mock_result.scalars().all.return_value = [record1, record2]
        mock_db_session.execute.return_value = mock_result

        service = FuelRecordService(mock_db_session)
        records = await service.list_fuel_records(user_id=user_id, vehicle_id=vehicle_id)

        assert len(records) == 2
        assert records[0].fuel_type == "ハイオク"
        assert records[1].fuel_type == "レギュラー"


class TestFuelRecordServiceCreateFuelRecord:
    """FuelRecordService.create_fuel_record テスト."""

    @pytest.mark.asyncio
    async def test_create_fuel_record_success(self, mock_db_session: AsyncMock) -> None:
        """燃費記録作成成功."""
        user_id = UUID("550e8400-e29b-41d4-a716-446655440000")
        vehicle_id = UUID("550e8400-e29b-41d4-a716-446655440001")
        now = datetime.now(JST)

        fuel_record_create = FuelRecordCreate(
            vehicle_id=vehicle_id,
            refuel_datetime=now,
            total_mileage=100,
            fuel_type="ハイオク",
            unit_price=165,
            total_cost=6600,
            is_full_tank=True,
            gas_station_name="ENEOS 1",
        )

        service = FuelRecordService(mock_db_session)
        result = await service.create_fuel_record(fuel_record_create, user_id)

        assert result.user_id == user_id
        assert result.vehicle_id == vehicle_id
        assert result.fuel_type == "ハイオク"

    @pytest.mark.asyncio
    async def test_create_fuel_record_with_minimal_fields(
        self, mock_db_session: AsyncMock
    ) -> None:
        """最小限フィールドで作成."""
        user_id = UUID("550e8400-e29b-41d4-a716-446655440000")
        vehicle_id = UUID("550e8400-e29b-41d4-a716-446655440001")
        now = datetime.now(JST)

        fuel_record_create = FuelRecordCreate(
            vehicle_id=vehicle_id,
            refuel_datetime=now,
            total_mileage=100,
            fuel_type="ハイオク",
            unit_price=165,
            total_cost=6600,
        )

        service = FuelRecordService(mock_db_session)
        result = await service.create_fuel_record(fuel_record_create, user_id)

        assert result.is_full_tank is False
        assert result.gas_station_name is None


class TestFuelRecordServiceUpdateFuelRecord:
    """FuelRecordService.update_fuel_record テスト."""

    @pytest.mark.asyncio
    async def test_update_fuel_record_success(self, mock_db_session: AsyncMock) -> None:
        """燃費記録更新成功."""
        user_id = UUID("550e8400-e29b-41d4-a716-446655440000")
        vehicle_id = UUID("550e8400-e29b-41d4-a716-446655440001")
        fuel_record_id = UUID("550e8400-e29b-41d4-a716-446655440101")
        now = datetime.now(JST)

        fuel_record = FuelRecord(
            id=fuel_record_id,
            vehicle_id=vehicle_id,
            user_id=user_id,
            refuel_datetime=now,
            total_mileage=100,
            fuel_type="ハイオク",
            unit_price=165,
            total_cost=6600,
            created_at=now,
            updated_at=now,
        )

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = fuel_record
        mock_db_session.execute.return_value = mock_result

        fuel_record_update = FuelRecordUpdate(fuel_type="レギュラー")

        service = FuelRecordService(mock_db_session)
        result = await service.update_fuel_record(
            fuel_record_id, fuel_record_update, user_id
        )

        assert result is not None
        assert result.fuel_type == "レギュラー"


class TestFuelRecordServiceDeleteFuelRecord:
    """FuelRecordService.delete_fuel_record テスト."""

    @pytest.mark.asyncio
    async def test_delete_fuel_record_success(self, mock_db_session: AsyncMock) -> None:
        """燃費記録削除成功."""
        user_id = UUID("550e8400-e29b-41d4-a716-446655440000")
        vehicle_id = UUID("550e8400-e29b-41d4-a716-446655440001")
        fuel_record_id = UUID("550e8400-e29b-41d4-a716-446655440101")
        now = datetime.now(JST)

        fuel_record = FuelRecord(
            id=fuel_record_id,
            vehicle_id=vehicle_id,
            user_id=user_id,
            refuel_datetime=now,
            total_mileage=100,
            fuel_type="ハイオク",
            unit_price=165,
            total_cost=6600,
            created_at=now,
            updated_at=now,
        )

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = fuel_record
        mock_db_session.execute.return_value = mock_result

        service = FuelRecordService(mock_db_session)
        result = await service.delete_fuel_record(fuel_record_id, user_id)

        assert result is True
        assert fuel_record.deleted_at is not None
