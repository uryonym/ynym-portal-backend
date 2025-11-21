"""Vehicle（車）スキーマバリデーションテスト."""

import pytest
from pydantic import ValidationError

from app.schemas.vehicle import VehicleCreate, VehicleUpdate


class TestVehicleCreateSchema:
    """VehicleCreate スキーマバリデーション."""

    def test_vehicle_create_valid_with_all_fields(self) -> None:
        """すべてのフィールド指定で有効."""
        schema = VehicleCreate(
            name="マイカー",
            maker="Toyota",
            model="Prius",
            year=2023,
            number="東京 123あ 1234",
            tank_capacity=50.0,
        )
        assert schema.name == "マイカー"
        assert schema.maker == "Toyota"
        assert schema.model == "Prius"
        assert schema.year == 2023
        assert schema.number == "東京 123あ 1234"
        assert schema.tank_capacity == 50.0

    def test_vehicle_create_valid_with_minimal_fields(self) -> None:
        """最小限のフィールドで有効."""
        schema = VehicleCreate(
            name="マイカー",
            maker="Toyota",
            model="Prius",
        )
        assert schema.name == "マイカー"
        assert schema.maker == "Toyota"
        assert schema.model == "Prius"
        assert schema.year is None
        assert schema.number is None
        assert schema.tank_capacity is None

    def test_vehicle_create_name_required(self) -> None:
        """車名は必須."""
        with pytest.raises(ValidationError):
            VehicleCreate(
                seq=1,
                maker="Toyota",
                model="Prius",
            )

    def test_vehicle_create_name_empty_fails(self) -> None:
        """車名が空文字列は不可."""
        with pytest.raises(ValidationError) as exc_info:
            VehicleCreate(
                name="",
                maker="Toyota",
                model="Prius",
            )
        assert "車名は必須項目です" in str(exc_info.value)

    def test_vehicle_create_name_whitespace_only_fails(self) -> None:
        """車名が空白のみは不可."""
        with pytest.raises(ValidationError) as exc_info:
            VehicleCreate(
                name="   ",
                maker="Toyota",
                model="Prius",
            )
        assert "車名は必須項目です" in str(exc_info.value)

    def test_vehicle_create_name_too_long_fails(self) -> None:
        """車名が 255 文字を超える場合は不可."""
        with pytest.raises(ValidationError) as exc_info:
            VehicleCreate(
                name="a" * 256,
                maker="Toyota",
                model="Prius",
            )
        assert "車名は 255 文字以内である必要があります" in str(exc_info.value)

    def test_vehicle_create_tank_capacity_positive(self) -> None:
        """タンク容量は正の数."""
        with pytest.raises(ValidationError) as exc_info:
            VehicleCreate(
                name="マイカー",
                maker="Toyota",
                model="Prius",
                tank_capacity=-50.0,
            )
        assert "タンク容量は 0 より大きい値である必要があります" in str(exc_info.value)

    def test_vehicle_create_name_whitespace_trimmed(self) -> None:
        """車名の前後の空白はトリム."""
        schema = VehicleCreate(
            name="  マイカー  ",
            maker="Toyota",
            model="Prius",
        )
        assert schema.name == "マイカー"

    def test_vehicle_create_number_whitespace_trimmed(self) -> None:
        """ナンバーの前後の空白はトリム."""
        schema = VehicleCreate(
            name="マイカー",
            maker="Toyota",
            model="Prius",
            number="  東京 123あ 1234  ",
        )
        assert schema.number == "東京 123あ 1234"


class TestVehicleUpdateSchema:
    """VehicleUpdate スキーマバリデーション."""

    def test_vehicle_update_all_fields_optional(self) -> None:
        """すべてのフィールドはオプション."""
        schema = VehicleUpdate()
        assert schema.name is None
        assert schema.seq is None
        assert schema.maker is None
        assert schema.model is None
        assert schema.year is None
        assert schema.number is None
        assert schema.tank_capacity is None

    def test_vehicle_update_partial_update_name_only(self) -> None:
        """特定のフィールドのみ更新可能."""
        schema = VehicleUpdate(name="新しい名前")
        assert schema.name == "新しい名前"
        assert schema.seq is None
        assert schema.maker is None

    def test_vehicle_update_name_empty_fails(self) -> None:
        """車名を空文字列に変更は不可."""
        with pytest.raises(ValidationError) as exc_info:
            VehicleUpdate(name="")
        assert "車名は空にできません" in str(exc_info.value)

    def test_vehicle_update_tank_capacity_positive(self) -> None:
        """タンク容量は正の数."""
        with pytest.raises(ValidationError) as exc_info:
            VehicleUpdate(tank_capacity=0)
        assert "タンク容量は 0 より大きい値である必要があります" in str(exc_info.value)
