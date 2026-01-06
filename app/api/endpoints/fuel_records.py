"""燃費記録関連エンドポイント."""

from datetime import timedelta, timezone
from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.fuel_record import (
    FuelRecordCreate,
    FuelRecordResponse,
    FuelRecordUpdate,
)
from app.security.deps import CurrentUser
from app.services.fuel_record_service import FuelRecordService
from app.utils.exceptions import NotFoundException

# 日本時間（JST）のタイムゾーン設定
JST = timezone(timedelta(hours=9))

router = APIRouter(
    prefix="/fuel-records",
    tags=["fuel-records"],
)


@router.get("", response_model=dict)
async def list_fuel_records(
    current_user: CurrentUser,
    vehicle_id: UUID = Query(..., description="車 ID"),
    skip: int = Query(0, ge=0, description="スキップするレコード数"),
    limit: int = Query(100, ge=1, le=1000, description="取得するレコード数"),
    db_session: AsyncSession = Depends(get_session),
) -> dict:
    """燃費記録一覧取得

    指定した車の燃費記録を取得します（新規順）

    Args:
        vehicle_id: 車 ID
        skip: スキップするレコード数（デフォルト 0）
        limit: 取得するレコード数（デフォルト 100、最大 1000）
        db_session: データベースセッション

    Returns:
        {
            "data": [FuelRecordResponse, ...],
            "message": "燃費記録一覧を取得しました"
        }
    """
    service = FuelRecordService(db_session)
    fuel_records = await service.list_fuel_records(
        user_id=current_user.id,
        vehicle_id=vehicle_id,
        limit=limit,
        offset=skip,
    )

    fuel_record_responses = [
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
        for item in fuel_records
    ]

    return {
        "data": fuel_record_responses,
        "message": "燃費記録一覧を取得しました",
    }


@router.post("", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_fuel_record(
    current_user: CurrentUser,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """燃費記録作成

    リクエスト本体に FuelRecordCreate スキーマで指定された燃費記録情報を使用して
    新規燃費記録を作成します。作成された燃費記録はレスポンス本体に返されます

    Args:
        request: リクエストオブジェクト
        db_session: データベースセッション

    Returns:
        {
            "data": FuelRecordResponse,
            "message": "燃費記録が作成されました"
        }

    Raises:
        422: リクエストボディのバリデーションエラー
    """
    try:
        # JSON をパースして FuelRecordCreate にバリデーション
        body = await request.json()
        fuel_record_create = FuelRecordCreate(**body)
    except ValidationError as e:
        # Pydantic バリデーションエラーを 400 で返す
        error_messages = []
        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "unknown"
            msg = error["msg"]
            error_messages.append(f"{field}: {msg}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "errors": error_messages,
                "message": "入力データが正しくありません",
            },
        )
    except Exception as e:
        # JSON パースエラーなど
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "errors": [str(e)],
                "message": "リクエストボディが不正です",
            },
        )

    service = FuelRecordService(db_session)
    fuel_record = await service.create_fuel_record(fuel_record_create, current_user.id)

    fuel_record_response = FuelRecordResponse.model_validate(fuel_record)

    return {
        "data": fuel_record_response,
        "message": "燃費記録が作成されました",
    }


@router.get("/{fuel_record_id}", response_model=None)
async def get_fuel_record(
    current_user: CurrentUser,
    fuel_record_id: UUID,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """燃費記録取得

    指定した ID の燃費記録を取得します

    Args:
        fuel_record_id: 燃費記録 ID
        db_session: データベースセッション

    Returns:
        {
            "data": FuelRecordResponse,
            "message": "燃費記録が取得されました"
        }

    Raises:
        404: 燃費記録が見つかりません
    """
    service = FuelRecordService(db_session)
    try:
        fuel_record = await service.get_fuel_record(fuel_record_id, current_user.id)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": "燃費記録が見つかりません",
            },
        )

    fuel_record_response = FuelRecordResponse.model_validate(fuel_record)

    return {
        "data": fuel_record_response,
        "message": "燃費記録が取得されました",
    }


@router.put("/{fuel_record_id}", response_model=None)
async def update_fuel_record(
    current_user: CurrentUser,
    fuel_record_id: UUID,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """燃費記録更新

    指定された燃費記録 ID の燃費記録情報を更新します
    リクエスト本体で指定されたフィールドのみが更新されます

    Args:
        fuel_record_id: 燃費記録 ID
        request: リクエストオブジェクト
        db_session: データベースセッション

    Returns:
        {
            "data": FuelRecordResponse,
            "message": "燃費記録が更新されました"
        }

    Raises:
        400: リクエストボディのバリデーションエラー
        404: 燃費記録が見つかりません
    """
    try:
        # JSON をパースして FuelRecordUpdate にバリデーション
        body = await request.json()
        fuel_record_update = FuelRecordUpdate(**body)
    except ValidationError as e:
        # Pydantic バリデーションエラーを 400 で返す
        error_messages = []
        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "unknown"
            msg = error["msg"]
            error_messages.append(f"{field}: {msg}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "errors": error_messages,
                "message": "入力データが正しくありません",
            },
        )
    except Exception as e:
        # JSON パースエラーなど
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "errors": [str(e)],
                "message": "リクエストボディが不正です",
            },
        )

    service = FuelRecordService(db_session)
    try:
        fuel_record = await service.update_fuel_record(
            fuel_record_id, fuel_record_update, current_user.id
        )
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": "燃費記録が見つかりません",
            },
        )

    fuel_record_response = FuelRecordResponse.model_validate(fuel_record)

    return {
        "data": fuel_record_response,
        "message": "燃費記録が更新されました",
    }


@router.delete(
    "/{fuel_record_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_fuel_record(
    current_user: CurrentUser,
    fuel_record_id: UUID,
    db_session: AsyncSession = Depends(get_session),
) -> Union[None, JSONResponse]:
    """燃費記録削除

    指定した燃費記録を削除します（論理削除）

    Args:
        fuel_record_id: 燃費記録 ID
        db_session: データベースセッション

    Returns:
        204 No Content

    Raises:
        404: 燃費記録が見つかりません
    """
    service = FuelRecordService(db_session)
    try:
        await service.delete_fuel_record(fuel_record_id, current_user.id)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": "燃費記録が見つかりません",
            },
        )

    return None
