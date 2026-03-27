"""ノートカテゴリ関連エンドポイント."""

from typing import List, Union
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_session
from app.repositories.note_category_repository import NoteCategoryRepository
from app.repositories.note_repository import NoteRepository
from app.schemas.note_category import NoteCategoryCreate, NoteCategoryResponse, NoteCategoryUpdate
from app.security.deps import CurrentUser
from app.services.note_category_service import NoteCategoryService
from app.utils.exceptions import NotFoundException

router = APIRouter(prefix="/note-categories", tags=["note-categories"])


def _get_note_category_service(db: Session = Depends(get_session)) -> NoteCategoryService:
    return NoteCategoryService(NoteCategoryRepository(db), NoteRepository(db))


@router.get("", response_model=dict)
def list_categories(
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: NoteCategoryService = Depends(_get_note_category_service),
) -> dict:
    """カテゴリ一覧を取得."""
    categories = service.list_categories(user_id=current_user.id, skip=skip, limit=limit)
    return {"data": [NoteCategoryResponse.model_validate(c) for c in categories], "message": "カテゴリ一覧を取得しました"}


@router.post("", response_model=None, status_code=status.HTTP_201_CREATED)
def create_category(
    current_user: CurrentUser,
    body: dict = Body(default={}),
    service: NoteCategoryService = Depends(_get_note_category_service),
) -> Union[dict, JSONResponse]:
    """新規カテゴリを作成."""
    try:
        category_create = NoteCategoryCreate(**body)
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"errors": [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()], "message": "入力データが正しくありません"},
        )
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": [str(e)], "message": "リクエストボディが不正です"})

    created = service.create_category(category_create, current_user.id)
    return {"data": NoteCategoryResponse.model_validate(created), "message": "カテゴリが作成されました"}


@router.get("/{category_id}", response_model=None)
def get_category(
    current_user: CurrentUser,
    category_id: UUID,
    service: NoteCategoryService = Depends(_get_note_category_service),
) -> Union[dict, JSONResponse]:
    """カテゴリを取得."""
    try:
        category = service.get_category(category_id, current_user.id)
    except NotFoundException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": str(e), "message": "カテゴリが見つかりません"})
    return {"data": NoteCategoryResponse.model_validate(category), "message": "カテゴリが取得されました"}


@router.put("/{category_id}", response_model=None)
def update_category(
    current_user: CurrentUser,
    category_id: UUID,
    body: dict = Body(default={}),
    service: NoteCategoryService = Depends(_get_note_category_service),
) -> Union[dict, JSONResponse]:
    """カテゴリを更新."""
    try:
        category_update = NoteCategoryUpdate(**body)
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"errors": [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()], "message": "入力データが正しくありません"},
        )
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": [str(e)], "message": "リクエストボディが不正です"})

    try:
        updated = service.update_category(category_id, category_update, current_user.id)
    except NotFoundException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": str(e), "message": "カテゴリが見つかりません"})
    return {"data": NoteCategoryResponse.model_validate(updated), "message": "カテゴリが更新されました"}


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    current_user: CurrentUser,
    category_id: UUID,
    service: NoteCategoryService = Depends(_get_note_category_service),
) -> None:
    """カテゴリを削除."""
    try:
        service.delete_category(category_id, current_user.id)
    except NotFoundException:
        raise
