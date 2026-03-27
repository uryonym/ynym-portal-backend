"""車両関連エンドポイント."""

from typing import List, Union
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_session
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate
from app.security.deps import CurrentUser
from app.services.vehicle_service import VehicleService
from app.utils.exceptions import NotFoundException

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


def _get_vehicle_service(db: Session = Depends(get_session)) -> VehicleService:
    return VehicleService(VehicleRepository(db))


@router.get("", response_model=dict)
def list_vehicles(
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: VehicleService = Depends(_get_vehicle_service),
) -> dict:
    """所有する車両一覧を取得."""
    vehicles = service.list_vehicles(user_id=current_user.id, skip=skip, limit=limit)
    return {
        "data": [VehicleResponse.model_validate(v) for v in vehicles],
        "message": "車一覧を取得しました",
    }


@router.post("", response_model=None, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    current_user: CurrentUser,
    body: dict = Body(default={}),
    service: VehicleService = Depends(_get_vehicle_service),
) -> Union[dict, JSONResponse]:
    """新規車両を作成."""
    try:
        vehicle_create = VehicleCreate(**body)
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"errors": [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()], "message": "入力データが正しくありません"},
        )
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": [str(e)], "message": "リクエストボディが不正です"})

    created = service.create_vehicle(vehicle_create, current_user.id)
    return {"data": VehicleResponse.model_validate(created), "message": "車が作成されました"}


@router.get("/{vehicle_id}", response_model=None)
def get_vehicle(
    current_user: CurrentUser,
    vehicle_id: UUID,
    service: VehicleService = Depends(_get_vehicle_service),
) -> Union[dict, JSONResponse]:
    """車両を取得."""
    try:
        vehicle = service.get_vehicle(vehicle_id, current_user.id)
    except NotFoundException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": str(e), "message": "車が見つかりません"})
    return {"data": VehicleResponse.model_validate(vehicle), "message": "車が取得されました"}


@router.put("/{vehicle_id}", response_model=None)
def update_vehicle(
    current_user: CurrentUser,
    vehicle_id: UUID,
    body: dict = Body(default={}),
    service: VehicleService = Depends(_get_vehicle_service),
) -> Union[dict, JSONResponse]:
    """車両を更新."""
    try:
        vehicle_update = VehicleUpdate(**body)
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"errors": [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()], "message": "入力データが正しくありません"},
        )
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": [str(e)], "message": "リクエストボディが不正です"})

    try:
        updated = service.update_vehicle(vehicle_id, vehicle_update, current_user.id)
    except NotFoundException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": str(e), "message": "車が見つかりません"})
    return {"data": VehicleResponse.model_validate(updated), "message": "車が更新されました"}


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    current_user: CurrentUser,
    vehicle_id: UUID,
    service: VehicleService = Depends(_get_vehicle_service),
) -> None:
    """車両を削除."""
    try:
        service.delete_vehicle(vehicle_id, current_user.id)
    except NotFoundException:
        raise
