"""車両リポジトリ."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import asc, desc, select

from app.models.vehicle import Vehicle
from app.repositories.base import BaseRepository


class VehicleRepository(BaseRepository[Vehicle]):
    """車両に関するデータアクセスを担う."""

    def __init__(self, session) -> None:
        super().__init__(session, Vehicle)

    def list_by_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Vehicle]:
        """ユーザーの車両一覧を seq 昇順で取得."""
        stmt = (
            select(Vehicle)
            .where(Vehicle.user_id == user_id)
            .where(Vehicle.deleted_at.is_(None))
            .order_by(asc(Vehicle.seq))
            .offset(skip)
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_by_id_and_user(self, vehicle_id: UUID, user_id: UUID) -> Optional[Vehicle]:
        """vehicle_id と user_id で車両を取得（所有権確認）."""
        stmt = (
            select(Vehicle)
            .where(Vehicle.id == vehicle_id)
            .where(Vehicle.user_id == user_id)
            .where(Vehicle.deleted_at.is_(None))
        )
        return self.session.execute(stmt).scalars().one_or_none()

    def get_max_seq(self, user_id: UUID) -> int:
        """ユーザーの最大 seq を返す（車両がない場合は 0）."""
        stmt = (
            select(Vehicle)
            .where(Vehicle.user_id == user_id)
            .where(Vehicle.deleted_at.is_(None))
            .order_by(desc(Vehicle.seq))
            .limit(1)
        )
        last = self.session.execute(stmt).scalars().one_or_none()
        return last.seq if last else 0
