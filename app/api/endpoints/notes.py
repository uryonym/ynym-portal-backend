"""ノート関連エンドポイント."""

from typing import List, Union
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate
from app.security.deps import CurrentUser
from app.services.note_service import NoteService
from app.utils.exceptions import NotFoundException

router = APIRouter(prefix="/notes", tags=["notes"])


def _not_found_message(error: NotFoundException) -> str:
    """NotFoundExceptionの内容に応じてメッセージを返す."""
    return (
        "カテゴリが見つかりません"
        if "カテゴリ ID" in str(error)
        else "ノートが見つかりません"
    )


@router.get("", response_model=dict)
async def list_notes(
    current_user: CurrentUser,
    skip: int = Query(0, ge=0, description="スキップするレコード数"),
    limit: int = Query(100, ge=1, le=1000, description="取得するレコード数"),
    db_session: AsyncSession = Depends(get_session),
) -> dict:
    """ノート一覧を取得.

    既定の並び順はカテゴリ名の昇順、次にタイトルの昇順。
    カテゴリ未設定のノートは末尾に並びます。
    """
    service = NoteService(db_session)
    notes: List[Note] = await service.list_notes(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )

    note_responses = [NoteResponse.model_validate(note) for note in notes]

    return {
        "data": note_responses,
        "message": "ノート一覧を取得しました",
    }


@router.post("", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_note(
    current_user: CurrentUser,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """新規ノートを作成."""
    try:
        body = await request.json()
        note_create = NoteCreate(**body)
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

    service = NoteService(db_session)
    try:
        created_note = await service.create_note(note_create, current_user.id)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": _not_found_message(e),
            },
        )

    return {
        "data": NoteResponse.model_validate(created_note),
        "message": "ノートが作成されました",
    }


@router.get("/{note_id}", response_model=None)
async def get_note(
    current_user: CurrentUser,
    note_id: UUID,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """ノートを取得."""
    service = NoteService(db_session)
    try:
        note = await service.get_note(note_id, current_user.id)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": "ノートが見つかりません",
            },
        )

    return {
        "data": NoteResponse.model_validate(note),
        "message": "ノートが取得されました",
    }


@router.put("/{note_id}", response_model=None)
async def update_note(
    current_user: CurrentUser,
    note_id: UUID,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """ノートを更新."""
    try:
        body = await request.json()
        note_update = NoteUpdate(**body)
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

    service = NoteService(db_session)
    try:
        updated_note = await service.update_note(note_id, note_update, current_user.id)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": _not_found_message(e),
            },
        )

    return {
        "data": NoteResponse.model_validate(updated_note),
        "message": "ノートが更新されました",
    }


@router.delete("/{note_id}", response_model=None)
async def delete_note(
    current_user: CurrentUser,
    note_id: UUID,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """ノートを削除."""
    service = NoteService(db_session)
    try:
        await service.delete_note(note_id, current_user.id)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": "ノートが見つかりません",
            },
        )

    return {
        "message": "ノートが削除されました",
    }
