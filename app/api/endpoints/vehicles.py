"""車両関連エンドポイント."""

import logging
from datetime import datetime, timedelta, timezone
from typing import List, Union
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

from app.database import get_session
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate
from app.services.vehicle_service import VehicleService
from app.security.deps import CurrentUser
from app.utils.exceptions import NotFoundException

# 日本時間（JST）のタイムゾーン設定
JST = timezone(timedelta(hours=9))

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("", response_model=dict)
async def list_vehicles(
    current_user: CurrentUser,
    skip: int = Query(0, ge=0, description="スキップするレコード数"),
    limit: int = Query(100, ge=1, le=1000, description="取得するレコード数"),
    db_session: AsyncSession = Depends(get_session),
) -> dict:
    """所有する車一覧を取得.

    作成日時の新しい順でソートされて返されます。

    Args:
        skip: スキップするレコード数（デフォルト 0）
        limit: 取得するレコード数（デフォルト 100、最大 1000）
        db_session: データベースセッション

    Returns:
        {
            "data": [VehicleResponse, ...],
            "message": "車一覧を取得しました"
        }
    """
    service = VehicleService(db_session)
    vehicles: List[Vehicle] = await service.list_vehicles(
        user_id=current_user.id, skip=skip, limit=limit
    )

    # Vehicle を VehicleResponse に変換
    vehicle_responses = [
        VehicleResponse(
            id=str(vehicle.id),
            user_id=str(vehicle.user_id),
            name=vehicle.name,
            seq=vehicle.seq,
            maker=vehicle.maker,
            model=vehicle.model,
            year=vehicle.year,
            number=vehicle.number,
            tank_capacity=vehicle.tank_capacity,
            created_at=vehicle.created_at.isoformat()
            if vehicle.created_at
            else datetime.now(JST).isoformat(),
            updated_at=vehicle.updated_at.isoformat()
            if vehicle.updated_at
            else datetime.now(JST).isoformat(),
        )
        for vehicle in vehicles
    ]

    return {
        "data": vehicle_responses,
        "message": "車一覧を取得しました",
    }


@router.post("", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    current_user: CurrentUser,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """新規車を作成.

    リクエスト本体に VehicleCreate スキーマで指定された車情報を使用して
    新規車を作成します。作成された車はレスポンス本体に返されます。

    Args:
        request: リクエストオブジェクト
        db_session: データベースセッション

    Returns:
        {
            "data": VehicleResponse,
            "message": "車が作成されました"
        }

    Raises:
        422: リクエストボディのバリデーションエラー
    """
    try:
        # JSON をパースして VehicleCreate にバリデーション
        body = await request.json()
        vehicle_create = VehicleCreate(**body)
    except ValidationError as e:
        # Pydantic バリデーションエラーを 400 で返す
        logger.error(f"VehicleCreate バリデーションエラー: {e.errors()}", exc_info=True)
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
        logger.error(f"リクエストボディパースエラー: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "errors": [str(e)],
                "message": "リクエストボディが不正です",
            },
        )

    service = VehicleService(db_session)
    created_vehicle: Vehicle = await service.create_vehicle(
        vehicle_create, current_user.id
    )

    # Vehicle を VehicleResponse に変換
    vehicle_response = VehicleResponse(
        id=str(created_vehicle.id),
        user_id=str(created_vehicle.user_id),
        name=created_vehicle.name,
        seq=created_vehicle.seq,
        maker=created_vehicle.maker,
        model=created_vehicle.model,
        year=created_vehicle.year,
        number=created_vehicle.number,
        tank_capacity=created_vehicle.tank_capacity,
        created_at=created_vehicle.created_at.isoformat()
        if created_vehicle.created_at
        else datetime.now(JST).isoformat(),
        updated_at=created_vehicle.updated_at.isoformat()
        if created_vehicle.updated_at
        else datetime.now(JST).isoformat(),
    )

    return {
        "data": vehicle_response,
        "message": "車が作成されました",
    }


@router.get("/{vehicle_id}", response_model=None)
async def get_vehicle(
    current_user: CurrentUser,
    vehicle_id: UUID,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """特定の車を取得.

    指定された車 ID の車情報を取得します。

    Args:
        vehicle_id: 車 ID
        db_session: データベースセッション

    Returns:
        {
            "data": VehicleResponse,
            "message": "車が取得されました"
        }

    Raises:
        404: 車が見つかりません
    """
    service = VehicleService(db_session)
    try:
        vehicle: Vehicle = await service.get_vehicle(vehicle_id, current_user.id)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": "車が見つかりません",
            },
        )

    # Vehicle を VehicleResponse に変換
    vehicle_response = VehicleResponse(
        id=str(vehicle.id),
        user_id=str(vehicle.user_id),
        name=vehicle.name,
        seq=vehicle.seq,
        maker=vehicle.maker,
        model=vehicle.model,
        year=vehicle.year,
        number=vehicle.number,
        tank_capacity=vehicle.tank_capacity,
        created_at=vehicle.created_at.isoformat()
        if vehicle.created_at
        else datetime.now(JST).isoformat(),
        updated_at=vehicle.updated_at.isoformat()
        if vehicle.updated_at
        else datetime.now(JST).isoformat(),
    )

    return {
        "data": vehicle_response,
        "message": "車が取得されました",
    }


@router.put("/{vehicle_id}", response_model=None)
async def update_vehicle(
    current_user: CurrentUser,
    vehicle_id: UUID,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """車情報を更新.

    指定された車 ID の車情報を更新します。
    リクエスト本体で指定されたフィールドのみが更新されます。

    Args:
        vehicle_id: 車 ID
        request: リクエストオブジェクト
        db_session: データベースセッション

    Returns:
        {
            "data": VehicleResponse,
            "message": "車が更新されました"
        }

    Raises:
        400: リクエストボディのバリデーションエラー
        404: 車が見つかりません
    """
    try:
        # JSON をパースして VehicleUpdate にバリデーション
        body = await request.json()
        vehicle_update = VehicleUpdate(**body)
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

    service = VehicleService(db_session)
    try:
        updated_vehicle: Vehicle = await service.update_vehicle(
            vehicle_id, vehicle_update, current_user.id
        )
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": "車が見つかりません",
            },
        )

    # Vehicle を VehicleResponse に変換
    vehicle_response = VehicleResponse(
        id=str(updated_vehicle.id),
        user_id=str(updated_vehicle.user_id),
        name=updated_vehicle.name,
        seq=updated_vehicle.seq,
        maker=updated_vehicle.maker,
        model=updated_vehicle.model,
        year=updated_vehicle.year,
        number=updated_vehicle.number,
        tank_capacity=updated_vehicle.tank_capacity,
        created_at=updated_vehicle.created_at.isoformat()
        if updated_vehicle.created_at
        else datetime.now(JST).isoformat(),
        updated_at=updated_vehicle.updated_at.isoformat()
        if updated_vehicle.updated_at
        else datetime.now(JST).isoformat(),
    )

    return {
        "data": vehicle_response,
        "message": "車が更新されました",
    }


@router.delete(
    "/{vehicle_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_vehicle(
    current_user: CurrentUser,
    vehicle_id: UUID,
    db_session: AsyncSession = Depends(get_session),
) -> Union[None, JSONResponse]:
    """車を削除.

    指定された車 ID の車を削除します。

    Args:
        vehicle_id: 車 ID
        db_session: データベースセッション

    Returns:
        204 No Content

    Raises:
        404: 車が見つかりません
    """
    service = VehicleService(db_session)
    try:
        await service.delete_vehicle(vehicle_id, current_user.id)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": "車が見つかりません",
            },
        )

    return None
