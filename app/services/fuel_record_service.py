"""燃費記録サービス."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.models.base import JST
from app.models.fuel_record import FuelRecord
from app.repositories.fuel_record_repository import FuelRecordRepository
from app.schemas.fuel_record import FuelRecordCreate, FuelRecordUpdate


@dataclass
class FuelRecordWithCalculation:
    """燃費計算結果付き燃費記録."""

    record: FuelRecord
    distance_traveled: Optional[int]
    fuel_amount: Optional[float]
    fuel_efficiency: Optional[float]


class FuelRecordService:
    """燃費記録管理ビジネスロジック層."""

    def __init__(self, fuel_record_repo: FuelRecordRepository) -> None:
        self.fuel_record_repo = fuel_record_repo

    def list_fuel_records(
        self,
        user_id: UUID,
        vehicle_id: Optional[UUID] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[FuelRecordWithCalculation]:
        """燃費記録一覧取得（燃費計算付き）."""
        records = self.fuel_record_repo.list_by_user_and_vehicle(
            user_id, vehicle_id, limit, offset
        )

        if vehicle_id and records:
            all_records = self.fuel_record_repo.list_all_by_vehicle_asc(user_id, vehicle_id)
            return self._calculate_fuel_efficiency(records, all_records)

        return [
            FuelRecordWithCalculation(
                record=r,
                distance_traveled=None,
                fuel_amount=None,
                fuel_efficiency=None,
            )
            for r in records
        ]

    def _calculate_fuel_efficiency(
        self,
        records: List[FuelRecord],
        all_records: List[FuelRecord],
    ) -> List[FuelRecordWithCalculation]:
        """燃費を計算して FuelRecordWithCalculation リストを返す."""
        prev_record_map: dict[UUID, Optional[FuelRecord]] = {}
        for i, rec in enumerate(all_records):
            prev_record_map[rec.id] = all_records[i - 1] if i > 0 else None

        results = []
        for record in records:
            prev_record = prev_record_map.get(record.id)

            distance_traveled = (
                record.total_mileage - prev_record.total_mileage
                if prev_record
                else record.total_mileage
            )

            fuel_amount: Optional[float] = None
            if record.unit_price > 0:
                fuel_amount = round(record.total_cost / record.unit_price, 2)

            fuel_efficiency: Optional[float] = None
            if fuel_amount and fuel_amount > 0:
                fuel_efficiency = round(distance_traveled / fuel_amount, 2)

            results.append(
                FuelRecordWithCalculation(
                    record=record,
                    distance_traveled=distance_traveled,
                    fuel_amount=fuel_amount,
                    fuel_efficiency=fuel_efficiency,
                )
            )

        return results

    def get_fuel_record(self, fuel_record_id: UUID, user_id: UUID) -> Optional[FuelRecord]:
        """燃費記録を取得（見つからない場合は None）."""
        return self.fuel_record_repo.get_by_id_and_user(fuel_record_id, user_id)

    def create_fuel_record(
        self, fuel_record_create: FuelRecordCreate, user_id: UUID
    ) -> FuelRecord:
        """燃費記録を作成."""
        fuel_record = FuelRecord(
            user_id=user_id,
            vehicle_id=fuel_record_create.vehicle_id,
            refuel_datetime=fuel_record_create.refuel_datetime,
            total_mileage=fuel_record_create.total_mileage,
            fuel_type=fuel_record_create.fuel_type,
            unit_price=fuel_record_create.unit_price,
            total_cost=fuel_record_create.total_cost,
            is_full_tank=fuel_record_create.is_full_tank,
            gas_station_name=fuel_record_create.gas_station_name,
        )
        return self.fuel_record_repo.save(fuel_record)

    def update_fuel_record(
        self,
        fuel_record_id: UUID,
        fuel_record_update: FuelRecordUpdate,
        user_id: UUID,
    ) -> Optional[FuelRecord]:
        """燃費記録を部分更新."""
        fuel_record = self.get_fuel_record(fuel_record_id, user_id)
        if not fuel_record:
            return None
        for key, value in fuel_record_update.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(fuel_record, key, value)
        return self.fuel_record_repo.save(fuel_record)

    def delete_fuel_record(self, fuel_record_id: UUID, user_id: UUID) -> bool:
        """燃費記録を論理削除."""
        fuel_record = self.get_fuel_record(fuel_record_id, user_id)
        if not fuel_record:
            return False
        fuel_record.deleted_at = datetime.now(JST)
        self.fuel_record_repo.save(fuel_record)
        return True
