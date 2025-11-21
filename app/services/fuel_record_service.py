"""燃費記録サービス."""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fuel_record import FuelRecord
from app.schemas.fuel_record import FuelRecordCreate, FuelRecordUpdate


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
    ) -> list[FuelRecord]:
        """燃費記録一覧取得.

        Args:
            user_id: ユーザー ID.
            vehicle_id: 車 ID（オプション）.
            limit: 取得件数.
            offset: オフセット.

        Returns:
            燃費記録リスト（新規順）.
        """
        query = select(FuelRecord).where(
            FuelRecord.user_id == user_id,
            FuelRecord.deleted_at.is_(None),
        )

        if vehicle_id:
            query = query.where(FuelRecord.vehicle_id == vehicle_id)

        query = query.order_by(FuelRecord.created_at.desc()).limit(limit).offset(offset)

        result = await self.db_session.execute(query)
        return result.scalars().all()

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
        await self.db_session.flush()
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
        await self.db_session.flush()
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

        from datetime import datetime, timedelta, timezone

        JST = timezone(timedelta(hours=9))
        fuel_record.deleted_at = datetime.now(JST)
        self.db_session.add(fuel_record)
        await self.db_session.flush()
        return True
