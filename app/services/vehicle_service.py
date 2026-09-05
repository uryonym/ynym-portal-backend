"""Vehicle（車）管理サービス."""

from datetime import datetime
from typing import List
from uuid import UUID

from app.models.base import JST
from app.models.vehicle import Vehicle
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from app.utils.exceptions import NotFoundException


class VehicleService:
    """車両管理ビジネスロジック層."""

    def __init__(self, vehicle_repo: VehicleRepository) -> None:
        self.vehicle_repo = vehicle_repo

    def list_vehicles(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """ユーザーの車両一覧を取得."""
        return self.vehicle_repo.list_by_user(user_id, skip, limit)

    def get_vehicle(self, vehicle_id: UUID, user_id: UUID) -> Vehicle:
        """車両を ID で取得.

        Raises:
            NotFoundException: 車両が存在しない場合
        """
        vehicle = self.vehicle_repo.get_by_id_and_user(vehicle_id, user_id)
        if not vehicle:
            raise NotFoundException(f"車 ID {vehicle_id} が見つかりません")
        return vehicle

    def create_vehicle(self, vehicle_create: VehicleCreate, user_id: UUID) -> Vehicle:
        """新規車両を作成（seq はユーザー内で自動採番）."""
        next_seq = self.vehicle_repo.get_max_seq(user_id) + 1
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
        return self.vehicle_repo.save(vehicle)

    def update_vehicle(
        self,
        vehicle_id: UUID,
        vehicle_update: VehicleUpdate,
        user_id: UUID,
    ) -> Vehicle:
        """車両情報を部分更新."""
        vehicle = self.get_vehicle(vehicle_id, user_id)
        for field, value in vehicle_update.model_dump(exclude_unset=True).items():
            setattr(vehicle, field, value)
        return self.vehicle_repo.save(vehicle)

    def delete_vehicle(self, vehicle_id: UUID, user_id: UUID) -> None:
        """車両を論理削除."""
        vehicle = self.get_vehicle(vehicle_id, user_id)
        vehicle.deleted_at = datetime.now(JST)
        self.vehicle_repo.save(vehicle)
