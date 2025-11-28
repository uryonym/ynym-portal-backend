"""Vehicle（車）管理サービス."""

from typing import List
from uuid import UUID

from sqlalchemy import and_, asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from app.utils.exceptions import NotFoundException


class VehicleService:
    """車管理サービス."""

    def __init__(self, db_session: AsyncSession) -> None:
        """初期化.

        Args:
            db_session: データベースセッション
        """
        self.db_session = db_session

    async def list_vehicles(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Vehicle]:
        """ユーザーが所有する車一覧を取得.

        Args:
            user_id: ユーザー ID
            skip: スキップするレコード数
            limit: 取得するレコード数

        Returns:
            Vehicle のリスト
        """
        stmt = (
            select(Vehicle)
            .where(
                and_(
                    Vehicle.user_id == user_id,
                    Vehicle.deleted_at.is_(None),
                )
            )
            .order_by(asc(Vehicle.seq))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_vehicle(self, vehicle_id: UUID, user_id: UUID) -> Vehicle:
        """特定の車を取得.

        Args:
            vehicle_id: 車 ID
            user_id: ユーザー ID

        Returns:
            Vehicle オブジェクト

        Raises:
            NotFoundException: 車が見つかりません
        """
        stmt = select(Vehicle).where(
            and_(
                Vehicle.id == vehicle_id,
                Vehicle.user_id == user_id,
                Vehicle.deleted_at.is_(None),
            )
        )
        result = await self.db_session.execute(stmt)
        vehicle = result.scalars().one_or_none()

        if not vehicle:
            raise NotFoundException(f"車 ID {vehicle_id} が見つかりません")

        return vehicle

    async def create_vehicle(
        self,
        vehicle_create: VehicleCreate,
        user_id: UUID,
    ) -> Vehicle:
        """新規車を作成.

        seq（シーケンス番号）はユーザーが所有する車の中で自動採番されます。

        Args:
            vehicle_create: 車作成スキーマ
            user_id: ユーザー ID

        Returns:
            作成された Vehicle オブジェクト
        """
        # ユーザーが既に所有している車の最大 seq を取得
        stmt = (
            select(Vehicle)
            .where(
                and_(
                    Vehicle.user_id == user_id,
                    Vehicle.deleted_at.is_(None),
                )
            )
            .order_by(desc(Vehicle.seq))
            .limit(1)
        )
        result = await self.db_session.execute(stmt)
        last_vehicle = result.scalars().one_or_none()

        # 新しい seq を決定（既存最大値 + 1、存在しない場合は 1）
        next_seq = (last_vehicle.seq + 1) if last_vehicle else 1

        vehicle = Vehicle(
            user_id=user_id,
            name=vehicle_create.name,
            seq=next_seq,
            maker=vehicle_create.maker,
            model=vehicle_create.model,
            year=vehicle_create.year,
            number=vehicle_create.number,
            tank_capacity=vehicle_create.tank_capacity,
        )
        self.db_session.add(vehicle)
        await self.db_session.commit()
        await self.db_session.refresh(vehicle)
        return vehicle

    async def update_vehicle(
        self,
        vehicle_id: UUID,
        vehicle_update: VehicleUpdate,
        user_id: UUID,
    ) -> Vehicle:
        """車情報を更新.

        Args:
            vehicle_id: 車 ID
            vehicle_update: 車更新スキーマ
            user_id: ユーザー ID

        Returns:
            更新された Vehicle オブジェクト

        Raises:
            NotFoundException: 車が見つかりません
        """
        vehicle = await self.get_vehicle(vehicle_id, user_id)

        # 部分更新: 指定されたフィールドのみ更新
        update_data = vehicle_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(vehicle, field, value)

        self.db_session.add(vehicle)
        await self.db_session.commit()
        await self.db_session.refresh(vehicle)
        return vehicle

    async def delete_vehicle(self, vehicle_id: UUID, user_id: UUID) -> None:
        """車を削除（論理削除）.

        Args:
            vehicle_id: 車 ID
            user_id: ユーザー ID

        Raises:
            NotFoundException: 車が見つかりません
        """
        from datetime import datetime, timedelta, timezone

        vehicle = await self.get_vehicle(vehicle_id, user_id)

        # 論理削除
        JST = timezone(timedelta(hours=9))
        vehicle.deleted_at = datetime.now(JST)

        self.db_session.add(vehicle)
        await self.db_session.commit()
