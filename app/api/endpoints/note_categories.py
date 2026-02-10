"""ノートカテゴリ関連エンドポイント."""

from typing import List, Union
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.note_category import NoteCategory
from app.schemas.note_category import (
    NoteCategoryCreate,
    NoteCategoryResponse,
    NoteCategoryUpdate,
)
from app.security.deps import CurrentUser
from app.services.note_category_service import NoteCategoryService
from app.utils.exceptions import NotFoundException

router = APIRouter(prefix="/note-categories", tags=["note-categories"])


@router.get("", response_model=dict)
async def list_categories(
    current_user: CurrentUser,
    skip: int = Query(0, ge=0, description="スキップするレコード数"),
    limit: int = Query(100, ge=1, le=1000, description="取得するレコード数"),
    db_session: AsyncSession = Depends(get_session),
) -> dict:
    """カテゴリ一覧を取得."""
    service = NoteCategoryService(db_session)
    categories: List[NoteCategory] = await service.list_categories(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )

    category_responses = [
        NoteCategoryResponse.model_validate(category) for category in categories
    ]

    return {
        "data": category_responses,
        "message": "カテゴリ一覧を取得しました",
    }


@router.post("", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_category(
    current_user: CurrentUser,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """新規カテゴリを作成."""
    try:
        body = await request.json()
        category_create = NoteCategoryCreate(**body)
    except ValidationError as e:
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
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "errors": [str(e)],
                "message": "リクエストボディが不正です",
            },
        )

    service = NoteCategoryService(db_session)
    created_category = await service.create_category(category_create, current_user.id)

    return {
        "data": NoteCategoryResponse.model_validate(created_category),
        "message": "カテゴリが作成されました",
    }


@router.get("/{category_id}", response_model=None)
async def get_category(
    current_user: CurrentUser,
    category_id: UUID,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """カテゴリを取得."""
    service = NoteCategoryService(db_session)
    try:
        category = await service.get_category(category_id, current_user.id)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": "カテゴリが見つかりません",
            },
        )

    return {
        "data": NoteCategoryResponse.model_validate(category),
        "message": "カテゴリが取得されました",
    }


@router.put("/{category_id}", response_model=None)
async def update_category(
    current_user: CurrentUser,
    category_id: UUID,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """カテゴリを更新."""
    try:
        body = await request.json()
        category_update = NoteCategoryUpdate(**body)
    except ValidationError as e:
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
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "errors": [str(e)],
                "message": "リクエストボディが不正です",
            },
        )

    service = NoteCategoryService(db_session)
    try:
        updated_category = await service.update_category(
            category_id, category_update, current_user.id
        )
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": "カテゴリが見つかりません",
            },
        )

    return {
        "data": NoteCategoryResponse.model_validate(updated_category),
        "message": "カテゴリが更新されました",
    }


@router.delete("/{category_id}", response_model=None)
async def delete_category(
    current_user: CurrentUser,
    category_id: UUID,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """カテゴリを削除."""
    service = NoteCategoryService(db_session)
    try:
        await service.delete_category(category_id, current_user.id)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": "カテゴリが見つかりません",
            },
        )

    return {
        "message": "カテゴリが削除されました",
    }
