"""燃費記録リポジトリ."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import asc, desc, select

from app.models.fuel_record import FuelRecord
from app.repositories.base import BaseRepository


class FuelRecordRepository(BaseRepository[FuelRecord]):
    """燃費記録に関するデータアクセスを担う."""

    def __init__(self, session) -> None:
        super().__init__(session, FuelRecord)

    def list_by_user_and_vehicle(
        self,
        user_id: UUID,
        vehicle_id: Optional[UUID] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[FuelRecord]:
        """ユーザー（＋車両）の燃費記録を給油日時の降順で取得."""
        stmt = select(FuelRecord).where(
            FuelRecord.user_id == user_id,
            FuelRecord.deleted_at.is_(None),
        )
        if vehicle_id:
            stmt = stmt.where(FuelRecord.vehicle_id == vehicle_id)
        stmt = (
            stmt.order_by(desc(FuelRecord.refuel_datetime)).limit(limit).offset(offset)
        )
        return list(self.session.execute(stmt).scalars().all())

    def list_all_by_vehicle_asc(
        self, user_id: UUID, vehicle_id: UUID
    ) -> List[FuelRecord]:
        """燃費計算用: 指定車両の全レコードを給油日時昇順で取得."""
        stmt = (
            select(FuelRecord)
            .where(
                FuelRecord.user_id == user_id,
                FuelRecord.vehicle_id == vehicle_id,
                FuelRecord.deleted_at.is_(None),
            )
            .order_by(asc(FuelRecord.refuel_datetime))
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_by_id_and_user(
        self, record_id: UUID, user_id: UUID
    ) -> Optional[FuelRecord]:
        """record_id と user_id で燃費記録を取得（所有権確認）."""
        stmt = select(FuelRecord).where(
            FuelRecord.id == record_id,
            FuelRecord.user_id == user_id,
            FuelRecord.deleted_at.is_(None),
        )
        return self.session.execute(stmt).scalars().one_or_none()
