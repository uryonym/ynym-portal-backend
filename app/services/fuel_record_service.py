"""燃費記録サービス."""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from sqlalchemy import asc, select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fuel_record import FuelRecord
from app.schemas.fuel_record import FuelRecordCreate, FuelRecordUpdate


@dataclass
class FuelRecordWithCalculation:
    """燃費計算結果付き燃費記録."""

    record: FuelRecord
    distance_traveled: Optional[int]
    fuel_amount: Optional[float]
    fuel_efficiency: Optional[float]


class FuelRecordService:
    """燃費記録管理サービス.

    CRUD 操作とビジネスロジックを提供する.
    """

    def __init__(self, db_session: AsyncSession) -> None:
        """初期化.

        Args:
            db_session: データベースセッション.
        """
        self.db_session = db_session

    async def list_fuel_records(
        self,
        user_id: UUID,
        vehicle_id: Optional[UUID] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[FuelRecordWithCalculation]:
        """燃費記録一覧取得（燃費計算付き）.

        Args:
            user_id: ユーザー ID.
            vehicle_id: 車 ID（オプション）.
            limit: 取得件数.
            offset: オフセット.

        Returns:
            燃費計算結果付き燃費記録リスト（新規順）.
        """
        query = select(FuelRecord).where(
            FuelRecord.user_id == user_id,
            FuelRecord.deleted_at.is_(None),
        )

        if vehicle_id:
            query = query.where(FuelRecord.vehicle_id == vehicle_id)

        query = (
            query.order_by(desc(FuelRecord.refuel_datetime)).limit(limit).offset(offset)
        )

        result = await self.db_session.execute(query)
        records = list(result.scalars().all())

        # 燃費計算のため、同じ車両の全レコードを取得（給油日時の昇順）
        if vehicle_id and records:
            all_records_query = (
                select(FuelRecord)
                .where(
                    FuelRecord.user_id == user_id,
                    FuelRecord.vehicle_id == vehicle_id,
                    FuelRecord.deleted_at.is_(None),
                )
                .order_by(asc(FuelRecord.refuel_datetime))
            )
            all_result = await self.db_session.execute(all_records_query)
            all_records = list(all_result.scalars().all())

            return self._calculate_fuel_efficiency(records, all_records)

        # vehicle_id が指定されていない場合は計算なし
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
        records: list[FuelRecord],
        all_records: list[FuelRecord],
    ) -> list[FuelRecordWithCalculation]:
        """燃費を計算.

        Args:
            records: 返却対象のレコード.
            all_records: 同じ車両の全レコード（給油日時の昇順）.

        Returns:
            燃費計算結果付きレコードリスト.
        """
        # レコードIDから前回レコードへのマッピングを作成
        prev_record_map: dict[UUID, Optional[FuelRecord]] = {}
        for i, rec in enumerate(all_records):
            prev_record_map[rec.id] = all_records[i - 1] if i > 0 else None

        results = []
        for record in records:
            prev_record = prev_record_map.get(record.id)

            # 走行距離: 前回データがあれば差分、なければ総走行距離
            if prev_record:
                distance_traveled = record.total_mileage - prev_record.total_mileage
            else:
                distance_traveled = record.total_mileage

            # 給油量: 総費用 / 単価
            fuel_amount: Optional[float] = None
            if record.unit_price > 0:
                fuel_amount = round(record.total_cost / record.unit_price, 2)

            # 燃費: 走行距離 / 給油量（小数点2桁）
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

    async def get_fuel_record(
        self,
        fuel_record_id: UUID,
        user_id: UUID,
    ) -> Optional[FuelRecord]:
        """燃費記録取得.

        Args:
            fuel_record_id: 燃費記録 ID.
            user_id: ユーザー ID.

        Returns:
            燃費記録、見つからない場合は None.
        """
        query = select(FuelRecord).where(
            FuelRecord.id == fuel_record_id,
            FuelRecord.user_id == user_id,
            FuelRecord.deleted_at.is_(None),
        )

        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def create_fuel_record(
        self,
        fuel_record_create: FuelRecordCreate,
        user_id: UUID,
    ) -> FuelRecord:
        """燃費記録作成.

        Args:
            fuel_record_create: 作成データ.
            user_id: ユーザー ID.

        Returns:
            作成された燃費記録.
        """
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
        self.db_session.add(fuel_record)
        await self.db_session.commit()
        await self.db_session.refresh(fuel_record)
        return fuel_record

    async def update_fuel_record(
        self,
        fuel_record_id: UUID,
        fuel_record_update: FuelRecordUpdate,
        user_id: UUID,
    ) -> Optional[FuelRecord]:
        """燃費記録更新.

        Args:
            fuel_record_id: 燃費記録 ID.
            fuel_record_update: 更新データ.
            user_id: ユーザー ID.

        Returns:
            更新された燃費記録、見つからない場合は None.
        """
        fuel_record = await self.get_fuel_record(fuel_record_id, user_id)
        if not fuel_record:
            return None

        update_data = fuel_record_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(fuel_record, key, value)

        self.db_session.add(fuel_record)
        await self.db_session.commit()
        await self.db_session.refresh(fuel_record)
        return fuel_record

    async def delete_fuel_record(
        self,
        fuel_record_id: UUID,
        user_id: UUID,
    ) -> bool:
        """燃費記録削除（論理削除）.

        Args:
            fuel_record_id: 燃費記録 ID.
            user_id: ユーザー ID.

        Returns:
            削除成功時 True、見つからない場合 False.
        """
        fuel_record = await self.get_fuel_record(fuel_record_id, user_id)
        if not fuel_record:
            return False

        from datetime import datetime
        from app.models.base import JST

        fuel_record.deleted_at = datetime.now(JST)
        self.db_session.add(fuel_record)
        await self.db_session.commit()
        return True
