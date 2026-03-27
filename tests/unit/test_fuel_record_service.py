"""FuelRecordService unit tests (FuelRecordRepository mocked)."""

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock
from uuid import UUID

from app.models.fuel_record import FuelRecord
from app.repositories.fuel_record_repository import FuelRecordRepository
from app.schemas.fuel_record import FuelRecordCreate, FuelRecordUpdate
from app.services.fuel_record_service import FuelRecordService

JST = timezone(timedelta(hours=9))
USER_ID = UUID('550e8400-e29b-41d4-a716-446655440000')
VEHICLE_ID = UUID('550e8400-e29b-41d4-a716-446655440001')
RECORD_ID = UUID('550e8400-e29b-41d4-a716-446655440101')


def _make_record(record_id, total_mileage, total_cost, unit_price, **kwargs):
    now = kwargs.pop('dt', datetime.now(JST))
    r = FuelRecord(
        vehicle_id=VEHICLE_ID,
        user_id=USER_ID,
        refuel_datetime=now,
        total_mileage=total_mileage,
        fuel_type='halogen',
        unit_price=unit_price,
        total_cost=total_cost,
        **kwargs,
    )
    r.id = record_id
    return r


@pytest.fixture
def mock_repo():
    repo = MagicMock(spec=FuelRecordRepository)
    repo.save.side_effect = lambda obj: obj
    return repo


class TestFuelRecordServiceListFuelRecords:
    """list_fuel_records tests."""

    def test_empty_list(self, mock_repo):
        """Returns empty list when no records."""
        mock_repo.list_by_user_and_vehicle.return_value = []
        service = FuelRecordService(mock_repo)
        result = service.list_fuel_records(user_id=USER_ID, vehicle_id=VEHICLE_ID)
        assert result == []
        mock_repo.list_all_by_vehicle_asc.assert_not_called()

    def test_single_record_uses_total_mileage(self, mock_repo):
        """First record uses total_mileage as distance."""
        record = _make_record(RECORD_ID, total_mileage=500, total_cost=8500, unit_price=170)
        mock_repo.list_by_user_and_vehicle.return_value = [record]
        mock_repo.list_all_by_vehicle_asc.return_value = [record]
        service = FuelRecordService(mock_repo)
        results = service.list_fuel_records(user_id=USER_ID, vehicle_id=VEHICLE_ID)
        assert len(results) == 1
        assert results[0].distance_traveled == 500
        assert results[0].fuel_amount == 50.0
        assert results[0].fuel_efficiency == 10.0

    def test_two_records_calculates_diff(self, mock_repo):
        """Difference between records is distance traveled."""
        now = datetime.now(JST)
        yesterday = now - timedelta(days=1)
        old = _make_record(
            UUID('aaaaaaaa-0000-0000-0000-000000000001'),
            total_mileage=500, total_cost=8250, unit_price=165, dt=yesterday,
        )
        new = _make_record(
            UUID('aaaaaaaa-0000-0000-0000-000000000002'),
            total_mileage=1000, total_cost=8500, unit_price=170, dt=now,
        )
        mock_repo.list_by_user_and_vehicle.return_value = [new]
        mock_repo.list_all_by_vehicle_asc.return_value = [old, new]
        service = FuelRecordService(mock_repo)
        results = service.list_fuel_records(user_id=USER_ID, vehicle_id=VEHICLE_ID)
        assert results[0].distance_traveled == 500
        assert results[0].fuel_amount == 50.0
        assert results[0].fuel_efficiency == 10.0

    def test_fuel_efficiency_rounded(self, mock_repo):
        """Fuel efficiency rounded to 2 decimal places."""
        record = _make_record(RECORD_ID, total_mileage=450, total_cost=8330, unit_price=170)
        mock_repo.list_by_user_and_vehicle.return_value = [record]
        mock_repo.list_all_by_vehicle_asc.return_value = [record]
        service = FuelRecordService(mock_repo)
        results = service.list_fuel_records(user_id=USER_ID, vehicle_id=VEHICLE_ID)
        assert results[0].fuel_amount == 49.0
        assert results[0].fuel_efficiency == 9.18

    def test_no_vehicle_id_skips_calculation(self, mock_repo):
        """Without vehicle_id, calculation fields are None."""
        record = _make_record(RECORD_ID, total_mileage=500, total_cost=8500, unit_price=170)
        mock_repo.list_by_user_and_vehicle.return_value = [record]
        service = FuelRecordService(mock_repo)
        results = service.list_fuel_records(user_id=USER_ID)
        assert results[0].distance_traveled is None
        mock_repo.list_all_by_vehicle_asc.assert_not_called()


class TestFuelRecordServiceCreateFuelRecord:
    """create_fuel_record tests."""

    def test_create_success(self, mock_repo):
        """Creates a fuel record."""
        now = datetime.now(JST)
        data = FuelRecordCreate(
            vehicle_id=VEHICLE_ID, refuel_datetime=now, total_mileage=100,
            fuel_type='regular', unit_price=165, total_cost=6600,
            is_full_tank=True, gas_station_name='ENEOS',
        )
        service = FuelRecordService(mock_repo)
        result = service.create_fuel_record(data, USER_ID)
        assert result.user_id == USER_ID
        assert result.vehicle_id == VEHICLE_ID
        mock_repo.save.assert_called_once()

    def test_create_minimal(self, mock_repo):
        """Minimal fields: is_full_tank defaults to False."""
        now = datetime.now(JST)
        data = FuelRecordCreate(
            vehicle_id=VEHICLE_ID, refuel_datetime=now, total_mileage=100,
            fuel_type='regular', unit_price=165, total_cost=6600,
        )
        service = FuelRecordService(mock_repo)
        result = service.create_fuel_record(data, USER_ID)
        assert result.is_full_tank is False
        assert result.gas_station_name is None


class TestFuelRecordServiceUpdateFuelRecord:
    """update_fuel_record tests."""

    def test_update_success(self, mock_repo):
        """Updates a fuel record."""
        now = datetime.now(JST)
        rec = FuelRecord(
            vehicle_id=VEHICLE_ID, user_id=USER_ID, refuel_datetime=now,
            total_mileage=100, fuel_type='halogen', unit_price=165, total_cost=6600,
        )
        rec.id = RECORD_ID
        mock_repo.get_by_id_and_user.return_value = rec
        service = FuelRecordService(mock_repo)
        result = service.update_fuel_record(RECORD_ID, FuelRecordUpdate(total_mileage=200), USER_ID)
        assert result is not None
        assert result.total_mileage == 200

    def test_update_not_found_returns_none(self, mock_repo):
        """Returns None when record not found."""
        mock_repo.get_by_id_and_user.return_value = None
        service = FuelRecordService(mock_repo)
        result = service.update_fuel_record(RECORD_ID, FuelRecordUpdate(total_mileage=200), USER_ID)
        assert result is None


class TestFuelRecordServiceDeleteFuelRecord:
    """delete_fuel_record tests."""

    def test_delete_sets_deleted_at(self, mock_repo):
        """Logical delete sets deleted_at."""
        now = datetime.now(JST)
        rec = FuelRecord(
            vehicle_id=VEHICLE_ID, user_id=USER_ID, refuel_datetime=now,
            total_mileage=100, fuel_type='halogen', unit_price=165, total_cost=6600,
        )
        rec.id = RECORD_ID
        rec.deleted_at = None
        mock_repo.get_by_id_and_user.return_value = rec
        service = FuelRecordService(mock_repo)
        result = service.delete_fuel_record(RECORD_ID, USER_ID)
        assert result is True
        assert rec.deleted_at is not None

    def test_delete_not_found_returns_false(self, mock_repo):
        """Returns False when record not found."""
        mock_repo.get_by_id_and_user.return_value = None
        service = FuelRecordService(mock_repo)
        result = service.delete_fuel_record(RECORD_ID, USER_ID)
        assert result is False
