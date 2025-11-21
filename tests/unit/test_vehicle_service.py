"""Vehicle（車）サービス単体テスト."""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from app.services.vehicle_service import VehicleService
from app.utils.exceptions import NotFoundException

JST = timezone(timedelta(hours=9))
TEST_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")
TEST_VEHICLE_ID = UUID("550e8400-e29b-41d4-a716-446655440001")


@pytest.fixture
def mock_db_session() -> AsyncMock:
    """モック DB セッション."""
    return AsyncMock()


class TestVehicleServiceListVehicles:
    """list_vehicles メソッドテスト."""

    @pytest.mark.asyncio
    async def test_list_vehicles_empty(self, mock_db_session: AsyncMock) -> None:
        """車一覧が空の場合."""
        # モック設定
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = []
        mock_db_session.execute.return_value = mock_result

        service = VehicleService(mock_db_session)
        vehicles = await service.list_vehicles(TEST_USER_ID)

        assert vehicles == []

    @pytest.mark.asyncio
    async def test_list_vehicles_with_multiple_vehicles(
        self, mock_db_session: AsyncMock
    ) -> None:
        """複数の車がある場合."""
        # テスト用車データ
        vehicle1 = Vehicle(
            id=UUID("550e8400-e29b-41d4-a716-446655440001"),
            user_id=TEST_USER_ID,
            name="マイカー1",
            maker="Toyota",
            model="Prius",
            created_at=datetime.now(JST),
            updated_at=datetime.now(JST),
        )
        vehicle2 = Vehicle(
            id=UUID("550e8400-e29b-41d4-a716-446655440002"),
            user_id=TEST_USER_ID,
            name="マイカー2",
            maker="Honda",
            model="Fit",
            created_at=datetime.now(JST),
            updated_at=datetime.now(JST),
        )

        mock_result = MagicMock()
        mock_result.scalars().all.return_value = [vehicle1, vehicle2]
        mock_db_session.execute.return_value = mock_result

        service = VehicleService(mock_db_session)
        vehicles = await service.list_vehicles(TEST_USER_ID)

        assert len(vehicles) == 2
        assert vehicles[0].name == "マイカー1"
        assert vehicles[1].name == "マイカー2"


class TestVehicleServiceGetVehicle:
    """get_vehicle メソッドテスト."""

    @pytest.mark.asyncio
    async def test_get_vehicle_success(self, mock_db_session: AsyncMock) -> None:
        """車取得成功."""
        vehicle = Vehicle(
            id=TEST_VEHICLE_ID,
            user_id=TEST_USER_ID,
            name="マイカー",
            maker="Toyota",
            model="Prius",
            created_at=datetime.now(JST),
            updated_at=datetime.now(JST),
        )

        mock_result = MagicMock()
        mock_result.scalars().one_or_none.return_value = vehicle
        mock_db_session.execute.return_value = mock_result

        service = VehicleService(mock_db_session)
        retrieved_vehicle = await service.get_vehicle(TEST_VEHICLE_ID, TEST_USER_ID)

        assert retrieved_vehicle.id == TEST_VEHICLE_ID
        assert retrieved_vehicle.name == "マイカー"

    @pytest.mark.asyncio
    async def test_get_vehicle_not_found_fails(
        self, mock_db_session: AsyncMock
    ) -> None:
        """車が見つからない場合は例外."""
        mock_result = MagicMock()
        mock_result.scalars().one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result

        service = VehicleService(mock_db_session)

        with pytest.raises(NotFoundException) as exc_info:
            await service.get_vehicle(TEST_VEHICLE_ID, TEST_USER_ID)

        assert f"車 ID {TEST_VEHICLE_ID}" in str(exc_info.value)


class TestVehicleServiceCreateVehicle:
    """create_vehicle メソッドテスト."""

    @pytest.mark.asyncio
    async def test_create_vehicle_success(self, mock_db_session: AsyncMock) -> None:
        """車作成成功."""
        vehicle_create = VehicleCreate(
            name="マイカー",
            maker="Toyota",
            model="Prius",
            year=2023,
            number="東京 123あ 1234",
            tank_capacity=50.0,
        )

        # モック設定: execute の戻り値に one_or_none メソッドを追加
        mock_result = MagicMock()
        mock_result.scalars().one_or_none.return_value = None  # 最初の seq 取得で None
        mock_db_session.execute.return_value = mock_result

        # モック設定: add → commit → refresh の流れ
        async def mock_refresh(obj: Vehicle) -> None:
            obj.id = TEST_VEHICLE_ID
            obj.created_at = datetime.now(JST)
            obj.updated_at = datetime.now(JST)

        mock_db_session.refresh = mock_refresh

        service = VehicleService(mock_db_session)
        created_vehicle = await service.create_vehicle(vehicle_create, TEST_USER_ID)

        assert created_vehicle.name == "マイカー"
        assert created_vehicle.maker == "Toyota"
        assert created_vehicle.year == 2023
        assert created_vehicle.seq == 1  # 最初の車は seq=1

    @pytest.mark.asyncio
    async def test_create_vehicle_with_minimal_fields(
        self, mock_db_session: AsyncMock
    ) -> None:
        """最小限フィールドで作成."""
        vehicle_create = VehicleCreate(
            name="マイカー",
            maker="Toyota",
            model="Prius",
        )

        # モック設定: execute の戻り値に one_or_none メソッドを追加
        mock_result = MagicMock()
        mock_result.scalars().one_or_none.return_value = None  # 最初の seq 取得で None
        mock_db_session.execute.return_value = mock_result

        async def mock_refresh(obj: Vehicle) -> None:
            obj.id = TEST_VEHICLE_ID
            obj.created_at = datetime.now(JST)
            obj.updated_at = datetime.now(JST)

        mock_db_session.refresh = mock_refresh

        service = VehicleService(mock_db_session)
        created_vehicle = await service.create_vehicle(vehicle_create, TEST_USER_ID)

        assert created_vehicle.name == "マイカー"
        assert created_vehicle.year is None
        assert created_vehicle.number is None
        assert created_vehicle.seq == 1  # 最初の車は seq=1


class TestVehicleServiceUpdateVehicle:
    """update_vehicle メソッドテスト."""

    @pytest.mark.asyncio
    async def test_update_vehicle_success(self, mock_db_session: AsyncMock) -> None:
        """車更新成功."""
        original_vehicle = Vehicle(
            id=TEST_VEHICLE_ID,
            user_id=TEST_USER_ID,
            name="古い名前",
            maker="Toyota",
            model="Prius",
            created_at=datetime.now(JST),
            updated_at=datetime.now(JST),
        )

        # get_vehicle のモック
        mock_result = MagicMock()
        mock_result.scalars().one_or_none.return_value = original_vehicle
        mock_db_session.execute.return_value = mock_result

        # refresh のモック
        async def mock_refresh(obj: Vehicle) -> None:
            pass

        mock_db_session.refresh = mock_refresh

        vehicle_update = VehicleUpdate(name="新しい名前")

        service = VehicleService(mock_db_session)
        updated_vehicle = await service.update_vehicle(
            TEST_VEHICLE_ID, vehicle_update, TEST_USER_ID
        )

        assert updated_vehicle.name == "新しい名前"

    @pytest.mark.asyncio
    async def test_update_vehicle_partial(self, mock_db_session: AsyncMock) -> None:
        """車の部分更新（year のみ更新）."""
        original_vehicle = Vehicle(
            id=TEST_VEHICLE_ID,
            user_id=TEST_USER_ID,
            name="マイカー",
            maker="Toyota",
            model="Prius",
            year=2020,
            created_at=datetime.now(JST),
            updated_at=datetime.now(JST),
        )

        # get_vehicle のモック
        mock_result = MagicMock()
        mock_result.scalars().one_or_none.return_value = original_vehicle
        mock_db_session.execute.return_value = mock_result

        # refresh のモック
        async def mock_refresh(obj: Vehicle) -> None:
            pass

        mock_db_session.refresh = mock_refresh

        vehicle_update = VehicleUpdate(year=2023)

        service = VehicleService(mock_db_session)
        updated_vehicle = await service.update_vehicle(
            TEST_VEHICLE_ID, vehicle_update, TEST_USER_ID
        )

        # 更新したフィールド
        assert updated_vehicle.year == 2023
        # 更新していないフィールドは変わらない
        assert updated_vehicle.name == "マイカー"
        assert updated_vehicle.maker == "Toyota"
