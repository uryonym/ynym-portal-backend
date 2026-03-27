"""燃費記録関連エンドポイント."""

from typing import Union
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_session
from app.repositories.fuel_record_repository import FuelRecordRepository
from app.schemas.fuel_record import FuelRecordCreate, FuelRecordResponse, FuelRecordUpdate
from app.security.deps import CurrentUser
from app.services.fuel_record_service import FuelRecordService
from app.utils.exceptions import NotFoundException

router = APIRouter(prefix="/fuel-records", tags=["fuel-records"])


def _get_fuel_record_service(db: Session = Depends(get_session)) -> FuelRecordService:
    return FuelRecordService(FuelRecordRepository(db))


@router.get("", response_model=dict)
def list_fuel_records(
    current_user: CurrentUser,
    vehicle_id: UUID = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: FuelRecordService = Depends(_get_fuel_record_service),
) -> dict:
    """燃費記録一覧取得."""
    items = service.list_fuel_records(user_id=current_user.id, vehicle_id=vehicle_id, limit=limit, offset=skip)
    responses = [
        FuelRecordResponse(
            id=item.record.id,
            vehicle_id=item.record.vehicle_id,
            user_id=item.record.user_id,
            refuel_datetime=item.record.refuel_datetime,
            total_mileage=item.record.total_mileage,
            fuel_type=item.record.fuel_type,
            unit_price=item.record.unit_price,
            total_cost=item.record.total_cost,
            is_full_tank=item.record.is_full_tank,
            gas_station_name=item.record.gas_station_name,
            distance_traveled=item.distance_traveled,
            fuel_amount=item.fuel_amount,
            fuel_efficiency=item.fuel_efficiency,
            created_at=item.record.created_at,
            updated_at=item.record.updated_at,
        )
        for item in items
    ]
    return {"data": responses, "message": "燃費記録一覧を取得しました"}


@router.post("", response_model=None, status_code=status.HTTP_201_CREATED)
def create_fuel_record(
    current_user: CurrentUser,
    body: dict = Body(default={}),
    service: FuelRecordService = Depends(_get_fuel_record_service),
) -> Union[dict, JSONResponse]:
    """燃費記録を作成."""
    try:
        fuel_record_create = FuelRecordCreate(**body)
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"errors": [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()], "message": "入力データが正しくありません"},
        )
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": [str(e)], "message": "リクエストボディが不正です"})

    created = service.create_fuel_record(fuel_record_create, current_user.id)
    response = FuelRecordResponse(
        id=created.id, vehicle_id=created.vehicle_id, user_id=created.user_id,
        refuel_datetime=created.refuel_datetime, total_mileage=created.total_mileage,
        fuel_type=created.fuel_type, unit_price=created.unit_price, total_cost=created.total_cost,
        is_full_tank=created.is_full_tank, gas_station_name=created.gas_station_name,
        distance_traveled=None, fuel_amount=None, fuel_efficiency=None,
        created_at=created.created_at, updated_at=created.updated_at,
    )
    return {"data": response, "message": "燃費記録が作成されました"}


@router.get("/{fuel_record_id}", response_model=None)
def get_fuel_record(
    current_user: CurrentUser,
    fuel_record_id: UUID,
    service: FuelRecordService = Depends(_get_fuel_record_service),
) -> Union[dict, JSONResponse]:
    """燃費記録を取得."""
    record = service.get_fuel_record(fuel_record_id, current_user.id)
    if not record:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "燃費記録が見つかりません"})
    response = FuelRecordResponse(
        id=record.id, vehicle_id=record.vehicle_id, user_id=record.user_id,
        refuel_datetime=record.refuel_datetime, total_mileage=record.total_mileage,
        fuel_type=record.fuel_type, unit_price=record.unit_price, total_cost=record.total_cost,
        is_full_tank=record.is_full_tank, gas_station_name=record.gas_station_name,
        distance_traveled=None, fuel_amount=None, fuel_efficiency=None,
        created_at=record.created_at, updated_at=record.updated_at,
    )
    return {"data": response, "message": "燃費記録を取得しました"}


@router.put("/{fuel_record_id}", response_model=None)
def update_fuel_record(
    current_user: CurrentUser,
    fuel_record_id: UUID,
    body: dict = Body(default={}),
    service: FuelRecordService = Depends(_get_fuel_record_service),
) -> Union[dict, JSONResponse]:
    """燃費記録を更新."""
    try:
        fuel_record_update = FuelRecordUpdate(**body)
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"errors": [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()], "message": "入力データが正しくありません"},
        )
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": [str(e)], "message": "リクエストボディが不正です"})

    updated = service.update_fuel_record(fuel_record_id, fuel_record_update, current_user.id)
    if not updated:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "燃費記録が見つかりません"})
    response = FuelRecordResponse(
        id=updated.id, vehicle_id=updated.vehicle_id, user_id=updated.user_id,
        refuel_datetime=updated.refuel_datetime, total_mileage=updated.total_mileage,
        fuel_type=updated.fuel_type, unit_price=updated.unit_price, total_cost=updated.total_cost,
        is_full_tank=updated.is_full_tank, gas_station_name=updated.gas_station_name,
        distance_traveled=None, fuel_amount=None, fuel_efficiency=None,
        created_at=updated.created_at, updated_at=updated.updated_at,
    )
    return {"data": response, "message": "燃費記録が更新されました"}


@router.delete("/{fuel_record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fuel_record(
    current_user: CurrentUser,
    fuel_record_id: UUID,
    service: FuelRecordService = Depends(_get_fuel_record_service),
) -> None:
    """燃費記録を削除."""
    deleted = service.delete_fuel_record(fuel_record_id, current_user.id)
    if not deleted:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="燃費記録が見つかりません")
