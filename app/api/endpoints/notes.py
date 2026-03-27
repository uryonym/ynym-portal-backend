"""ノート関連エンドポイント."""

from typing import List, Union
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_session
from app.repositories.note_category_repository import NoteCategoryRepository
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate
from app.security.deps import CurrentUser
from app.services.note_service import NoteService
from app.utils.exceptions import NotFoundException

router = APIRouter(prefix="/notes", tags=["notes"])


def _get_note_service(db: Session = Depends(get_session)) -> NoteService:
    return NoteService(NoteRepository(db), NoteCategoryRepository(db))


def _not_found_message(error: NotFoundException) -> str:
    return "カテゴリが見つかりません" if "カテゴリ ID" in str(error) else "ノートが見つかりません"


@router.get("", response_model=dict)
def list_notes(
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: NoteService = Depends(_get_note_service),
) -> dict:
    """ノート一覧を取得."""
    notes = service.list_notes(user_id=current_user.id, skip=skip, limit=limit)
    return {"data": [NoteResponse.model_validate(n) for n in notes], "message": "ノート一覧を取得しました"}


@router.post("", response_model=None, status_code=status.HTTP_201_CREATED)
def create_note(
    current_user: CurrentUser,
    body: dict = Body(default={}),
    service: NoteService = Depends(_get_note_service),
) -> Union[dict, JSONResponse]:
    """新規ノートを作成."""
    try:
        note_create = NoteCreate(**body)
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"errors": [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()], "message": "入力データが正しくありません"},
        )
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": [str(e)], "message": "リクエストボディが不正です"})

    try:
        created = service.create_note(note_create, current_user.id)
    except NotFoundException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": str(e), "message": _not_found_message(e)})
    return {"data": NoteResponse.model_validate(created), "message": "ノートが作成されました"}


@router.get("/{note_id}", response_model=None)
def get_note(
    current_user: CurrentUser,
    note_id: UUID,
    service: NoteService = Depends(_get_note_service),
) -> Union[dict, JSONResponse]:
    """ノートを取得."""
    try:
        note = service.get_note(note_id, current_user.id)
    except NotFoundException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": str(e), "message": "ノートが見つかりません"})
    return {"data": NoteResponse.model_validate(note), "message": "ノートが取得されました"}


@router.put("/{note_id}", response_model=None)
def update_note(
    current_user: CurrentUser,
    note_id: UUID,
    body: dict = Body(default={}),
    service: NoteService = Depends(_get_note_service),
) -> Union[dict, JSONResponse]:
    """ノートを更新."""
    try:
        note_update = NoteUpdate(**body)
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"errors": [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()], "message": "入力データが正しくありません"},
        )
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": [str(e)], "message": "リクエストボディが不正です"})

    try:
        updated = service.update_note(note_id, note_update, current_user.id)
    except NotFoundException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": str(e), "message": _not_found_message(e)})
    return {"data": NoteResponse.model_validate(updated), "message": "ノートが更新されました"}


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    current_user: CurrentUser,
    note_id: UUID,
    service: NoteService = Depends(_get_note_service),
) -> None:
    """ノートを削除."""
    try:
        service.delete_note(note_id, current_user.id)
    except NotFoundException:
        raise
