"""VehicleService ユニットテスト（VehicleRepository をモック）."""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from app.models.vehicle import Vehicle
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from app.services.vehicle_service import VehicleService
from app.utils.exceptions import NotFoundException

JST = timezone(timedelta(hours=9))
TEST_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")
TEST_VEHICLE_ID = UUID("550e8400-e29b-41d4-a716-446655440001")


def _make_vehicle(**kwargs) -> Vehicle:
    defaults = dict(
        id=TEST_VEHICLE_ID,
        user_id=TEST_USER_ID,
        name="マイカー",
        seq=1,
        maker="Toyota",
        model="Prius",
        year=None,
        number=None,
        tank_capacity=None,
        deleted_at=None,
        created_at=datetime.now(JST),
        updated_at=datetime.now(JST),
    )
    defaults.update(kwargs)
    v = Vehicle(**{k: defaults[k] for k in ["user_id", "name", "seq", "maker", "model"]})
    for k, val in defaults.items():
        object.__setattr__(v, k, val) if hasattr(v, k) else setattr(v, k, val)
    return v


@pytest.fixture
def mock_repo() -> MagicMock:
    repo = MagicMock(spec=VehicleRepository)
    repo.save.side_effect = lambda obj: obj
    return repo


class TestVehicleServiceListVehicles:
    """list_vehicles テスト."""

    def test_list_vehicles_empty(self, mock_repo: MagicMock) -> None:
        """車一覧が空の場合."""
        mock_repo.list_by_user.return_value = []
        service = VehicleService(mock_repo)
        assert service.list_vehicles(TEST_USER_ID) == []
        mock_repo.list_by_user.assert_called_once_with(TEST_USER_ID, 0, 100)

    def test_list_vehicles_multiple(self, mock_repo: MagicMock) -> None:
        """複数の車がある場合."""
        v1 = MagicMock(spec=Vehicle); v1.name = "マイカー1"
        v2 = MagicMock(spec=Vehicle); v2.name = "マイカー2"
        mock_repo.list_by_user.return_value = [v1, v2]
        service = VehicleService(mock_repo)
        result = service.list_vehicles(TEST_USER_ID)
        assert len(result) == 2
        assert result[0].name == "マイカー1"
        assert result[1].name == "マイカー2"


class TestVehicleServiceGetVehicle:
    """get_vehicle テスト."""

    def test_get_vehicle_success(self, mock_repo: MagicMock) -> None:
        """車取得成功."""
        vehicle = Vehicle(user_id=TEST_USER_ID, name="マイカー", seq=1, maker="Toyota", model="Prius")
        vehicle.id = TEST_VEHICLE_ID
        mock_repo.get_by_id_and_user.return_value = vehicle
        service = VehicleService(mock_repo)
        result = service.get_vehicle(TEST_VEHICLE_ID, TEST_USER_ID)
        assert result.name == "マイカー"

    def test_get_vehicle_not_found(self, mock_repo: MagicMock) -> None:
        """車が見つからない場合は例外."""
        mock_repo.get_by_id_and_user.return_value = None
        service = VehicleService(mock_repo)
        with pytest.raises(NotFoundException) as exc_info:
            service.get_vehicle(TEST_VEHICLE_ID, TEST_USER_ID)
        assert f"車 ID {TEST_VEHICLE_ID}" in str(exc_info.value)


class TestVehicleServiceCreateVehicle:
    """create_vehicle テスト."""

    def test_create_vehicle_success(self, mock_repo: MagicMock) -> None:
        """車作成成功（seq は get_max_seq + 1）."""
        mock_repo.get_max_seq.return_value = 0
        vehicle_create = VehicleCreate(name="マイカー", maker="Toyota", model="Prius", year=2023)
        service = VehicleService(mock_repo)
        result = service.create_vehicle(vehicle_create, TEST_USER_ID)
        assert result.name == "マイカー"
        assert result.seq == 1
        mock_repo.save.assert_called_once()

    def test_create_vehicle_seq_increments(self, mock_repo: MagicMock) -> None:
        """2台目は seq=2."""
        mock_repo.get_max_seq.return_value = 1
        vehicle_create = VehicleCreate(name="2台目", maker="Honda", model="Fit")
        service = VehicleService(mock_repo)
        result = service.create_vehicle(vehicle_create, TEST_USER_ID)
        assert result.seq == 2

    def test_create_vehicle_minimal_fields(self, mock_repo: MagicMock) -> None:
        """最小限フィールドで作成."""
        mock_repo.get_max_seq.return_value = 0
        vehicle_create = VehicleCreate(name="マイカー", maker="Toyota", model="Prius")
        service = VehicleService(mock_repo)
        result = service.create_vehicle(vehicle_create, TEST_USER_ID)
        assert result.year is None
        assert result.number is None
        assert result.seq == 1


class TestVehicleServiceUpdateVehicle:
    """update_vehicle テスト."""

    def test_update_vehicle_name(self, mock_repo: MagicMock) -> None:
        """名前を更新できる."""
        vehicle = Vehicle(user_id=TEST_USER_ID, name="古い名前", seq=1, maker="Toyota", model="Prius")
        mock_repo.get_by_id_and_user.return_value = vehicle
        service = VehicleService(mock_repo)
        result = service.update_vehicle(TEST_VEHICLE_ID, VehicleUpdate(name="新しい名前"), TEST_USER_ID)
        assert result.name == "新しい名前"
        mock_repo.save.assert_called_once()

    def test_update_vehicle_partial(self, mock_repo: MagicMock) -> None:
        """部分更新（year のみ）."""
        vehicle = Vehicle(user_id=TEST_USER_ID, name="マイカー", seq=1, maker="Toyota", model="Prius")
        vehicle.year = 2020
        mock_repo.get_by_id_and_user.return_value = vehicle
        service = VehicleService(mock_repo)
        result = service.update_vehicle(TEST_VEHICLE_ID, VehicleUpdate(year=2023), TEST_USER_ID)
        assert result.year == 2023
        assert result.name == "マイカー"

    def test_update_vehicle_not_found(self, mock_repo: MagicMock) -> None:
        """車が見つからない場合は例外."""
        mock_repo.get_by_id_and_user.return_value = None
        service = VehicleService(mock_repo)
        with pytest.raises(NotFoundException):
            service.update_vehicle(TEST_VEHICLE_ID, VehicleUpdate(name="X"), TEST_USER_ID)


class TestVehicleServiceDeleteVehicle:
    """delete_vehicle テスト."""

    def test_delete_vehicle_sets_deleted_at(self, mock_repo: MagicMock) -> None:
        """論理削除で deleted_at が設定される."""
        vehicle = Vehicle(user_id=TEST_USER_ID, name="マイカー", seq=1, maker="Toyota", model="Prius")
        vehicle.deleted_at = None
        mock_repo.get_by_id_and_user.return_value = vehicle
        service = VehicleService(mock_repo)
        service.delete_vehicle(TEST_VEHICLE_ID, TEST_USER_ID)
        assert vehicle.deleted_at is not None
        mock_repo.save.assert_called_once()

    def test_delete_vehicle_not_found(self, mock_repo: MagicMock) -> None:
        """車が見つからない場合は例外."""
        mock_repo.get_by_id_and_user.return_value = None
        service = VehicleService(mock_repo)
        with pytest.raises(NotFoundException):
            service.delete_vehicle(TEST_VEHICLE_ID, TEST_USER_ID)
