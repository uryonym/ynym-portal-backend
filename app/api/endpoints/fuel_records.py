"""燃費記録 API エンドポイント."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.fuel_record import (
    FuelRecordCreate,
    FuelRecordResponse,
    FuelRecordUpdate,
)
from app.services.fuel_record_service import FuelRecordService

router = APIRouter(
    prefix="/api/fuel-records",
    tags=["fuel-records"],
)


@router.get("", response_model=list[FuelRecordResponse], status_code=status.HTTP_200_OK)
async def list_fuel_records(
    vehicle_id: UUID = Query(..., description="車 ID"),
    limit: int = Query(100, ge=1, le=1000, description="取得件数"),
    offset: int = Query(0, ge=0, description="オフセット"),
    db_session: AsyncSession = Depends(get_session),
) -> list[FuelRecordResponse]:
    """燃費記録一覧取得.

    指定した車の燃費記録を取得します（新規順）.

    Args:
        vehicle_id: 車 ID.
        limit: 取得件数（デフォルト: 100）.
        offset: オフセット（デフォルト: 0）.
        db_session: データベースセッション.

    Returns:
        燃費記録リスト.
    """
    # TODO: 認証からユーザー ID を取得
    user_id = UUID("550e8400-e29b-41d4-a716-446655440000")

    service = FuelRecordService(db_session)
    fuel_records = await service.list_fuel_records(
        user_id=user_id,
        vehicle_id=vehicle_id,
        limit=limit,
        offset=offset,
    )

    return [FuelRecordResponse.model_validate(record) for record in fuel_records]


@router.post("", response_model=FuelRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_fuel_record(
    fuel_record_create: FuelRecordCreate,
    db_session: AsyncSession = Depends(get_session),
) -> FuelRecordResponse:
    """燃費記録作成.

    新しい燃費記録を作成します.

    Args:
        fuel_record_create: 燃費記録作成データ.
        db_session: データベースセッション.

    Returns:
        作成された燃費記録.
    """
    # TODO: 認証からユーザー ID を取得
    user_id = UUID("550e8400-e29b-41d4-a716-446655440000")

    service = FuelRecordService(db_session)
    fuel_record = await service.create_fuel_record(fuel_record_create, user_id)
    await db_session.commit()

    return FuelRecordResponse.model_validate(fuel_record)


@router.get(
    "/{fuel_record_id}",
    response_model=FuelRecordResponse,
    status_code=status.HTTP_200_OK,
)
async def get_fuel_record(
    fuel_record_id: UUID,
    db_session: AsyncSession = Depends(get_session),
) -> FuelRecordResponse:
    """燃費記録取得.

    指定した ID の燃費記録を取得します.

    Args:
        fuel_record_id: 燃費記録 ID.
        db_session: データベースセッション.

    Returns:
        燃費記録.

    Raises:
        HTTPException: 燃費記録が見つからない場合（404）.
    """
    # TODO: 認証からユーザー ID を取得
    user_id = UUID("550e8400-e29b-41d4-a716-446655440000")

    service = FuelRecordService(db_session)
    fuel_record = await service.get_fuel_record(fuel_record_id, user_id)

    if not fuel_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="燃費記録が見つかりません",
        )

    return FuelRecordResponse.model_validate(fuel_record)


@router.put(
    "/{fuel_record_id}",
    response_model=FuelRecordResponse,
    status_code=status.HTTP_200_OK,
)
async def update_fuel_record(
    fuel_record_id: UUID,
    fuel_record_update: FuelRecordUpdate,
    db_session: AsyncSession = Depends(get_session),
) -> FuelRecordResponse:
    """燃費記録更新.

    指定した燃費記録を更新します.

    Args:
        fuel_record_id: 燃費記録 ID.
        fuel_record_update: 更新データ.
        db_session: データベースセッション.

    Returns:
        更新された燃費記録.

    Raises:
        HTTPException: 燃費記録が見つからない場合（404）.
    """
    # TODO: 認証からユーザー ID を取得
    user_id = UUID("550e8400-e29b-41d4-a716-446655440000")

    service = FuelRecordService(db_session)
    fuel_record = await service.update_fuel_record(
        fuel_record_id, fuel_record_update, user_id
    )

    if not fuel_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="燃費記録が見つかりません",
        )

    await db_session.commit()
    return FuelRecordResponse.model_validate(fuel_record)


@router.delete("/{fuel_record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fuel_record(
    fuel_record_id: UUID,
    db_session: AsyncSession = Depends(get_session),
) -> None:
    """燃費記録削除.

    指定した燃費記録を削除します（論理削除）.

    Args:
        fuel_record_id: 燃費記録 ID.
        db_session: データベースセッション.

    Raises:
        HTTPException: 燃費記録が見つからない場合（404）.
    """
    # TODO: 認証からユーザー ID を取得
    user_id = UUID("550e8400-e29b-41d4-a716-446655440000")

    service = FuelRecordService(db_session)
    deleted = await service.delete_fuel_record(fuel_record_id, user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="燃費記録が見つかりません",
        )

    await db_session.commit()
