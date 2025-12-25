"""Task 関連エンドポイント."""

from datetime import datetime, timedelta, timezone
from typing import List, Optional, Union
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService
from app.security.deps import CurrentUser
from app.utils.exceptions import NotFoundException

# 日本時間（JST）のタイムゾーン設定
JST = timezone(timedelta(hours=9))

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=dict)
async def list_tasks(
    current_user: CurrentUser,
    skip: int = Query(0, ge=0, description="スキップするレコード数"),
    limit: int = Query(100, ge=1, le=1000, description="取得するレコード数"),
    is_completed: Optional[bool] = Query(
        None,
        description="完了状態でフィルタ（true: 完了のみ、false: 未完了のみ、指定なし: 全件）",
    ),
    db_session: AsyncSession = Depends(get_session),
) -> dict:
    """タスク一覧を取得.

    期日が近い順（昇順）でソートされ、期日なしのタスクは
    作成日時の古い順で期日ありのタスクの後に表示されます。

    Args:
        skip: スキップするレコード数（デフォルト 0）
        limit: 取得するレコード数（デフォルト 100、最大 1000）
        is_completed: 完了状態でフィルタ（true: 完了のみ、false: 未完了のみ、指定なし: 全件）
        db_session: データベースセッション

    Returns:
        {
            "data": [TaskResponse, ...],
            "message": "タスク一覧を取得しました"
        }
    """
    service = TaskService(db_session)
    tasks: List[Task] = await service.list_tasks(
        user_id=current_user.id, skip=skip, limit=limit, is_completed=is_completed
    )

    # Task を TaskResponse に変換
    task_responses = [
        TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            completed_at=task.completed_at,
            due_date=task.due_date,
            order=task.order,
            created_at=task.created_at or datetime.now(JST),
            updated_at=task.updated_at or datetime.now(JST),
        )
        for task in tasks
    ]

    return {
        "data": task_responses,
        "message": "タスク一覧を取得しました",
    }


@router.post("", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """新規タスクを作成.

    リクエスト本体に TaskCreate スキーマで指定されたタスク情報を使用して
    新規タスクを作成します。作成されたタスクはレスポンス本体に返されます。

    Args:
        request: リクエストオブジェクト
        db_session: データベースセッション

    Returns:
        {
            "data": TaskResponse,
            "message": "タスクが作成されました"
        }

    Raises:
        422: リクエストボディのバリデーションエラー
    """
    try:
        # JSON をパースして TaskCreate にバリデーション
        body = await request.json()
        task_create = TaskCreate(**body)
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

    service = TaskService(db_session)
    created_task: Task = await service.create_task(task_create, TEST_USER_ID)

    # Task を TaskResponse に変換
    task_response = TaskResponse(
        id=created_task.id,
        user_id=created_task.user_id,
        title=created_task.title,
        description=created_task.description,
        is_completed=created_task.is_completed,
        completed_at=created_task.completed_at,
        due_date=created_task.due_date,
        order=created_task.order,
        created_at=created_task.created_at or datetime.now(JST),
        updated_at=created_task.updated_at or datetime.now(JST),
    )

    return {
        "data": task_response,
        "message": "タスクが作成されました",
    }


@router.get("/{task_id}", response_model=None)
async def get_task(
    task_id: UUID,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """タスクを取得.

    指定されたタスク ID のタスク情報を取得します。

    Args:
        task_id: タスク ID
        db_session: データベースセッション

    Returns:
        {
            "data": TaskResponse,
            "message": "タスクが取得されました"
        }

    Raises:
        404: タスクが見つかりません
    """
    service = TaskService(db_session)
    try:
        task: Task = await service.get_task(task_id, TEST_USER_ID)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": "タスクが見つかりません",
            },
        )

    # Task を TaskResponse に変換
    task_response = TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        completed_at=task.completed_at,
        due_date=task.due_date,
        order=task.order,
        created_at=task.created_at or datetime.now(JST),
        updated_at=task.updated_at or datetime.now(JST),
    )

    return {
        "data": task_response,
        "message": "タスクが取得されました",
    }


@router.put("/{task_id}", response_model=None)
async def update_task(
    task_id: UUID,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> Union[dict, JSONResponse]:
    """タスクを更新.

    指定されたタスク ID のタスク情報を更新します。
    リクエスト本体で指定されたフィールドのみが更新されます。

    Args:
        task_id: タスク ID
        request: リクエストオブジェクト
        db_session: データベースセッション

    Returns:
        {
            "data": TaskResponse,
            "message": "タスクが更新されました"
        }

    Raises:
        400: リクエストボディのバリデーションエラー
        404: タスクが見つかりません
    """
    try:
        # JSON をパースして TaskUpdate にバリデーション
        body = await request.json()
        task_update = TaskUpdate(**body)
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

    service = TaskService(db_session)
    try:
        updated_task: Task = await service.update_task(
            task_id, task_update, TEST_USER_ID
        )
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": "タスクが見つかりません",
            },
        )

    # Task を TaskResponse に変換
    task_response = TaskResponse(
        id=updated_task.id,
        user_id=updated_task.user_id,
        title=updated_task.title,
        description=updated_task.description,
        is_completed=updated_task.is_completed,
        completed_at=updated_task.completed_at,
        due_date=updated_task.due_date,
        order=updated_task.order,
        created_at=updated_task.created_at or datetime.now(JST),
        updated_at=updated_task.updated_at or datetime.now(JST),
    )

    return {
        "data": task_response,
        "message": "タスクが更新されました",
    }


@router.delete(
    "/{task_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    task_id: UUID,
    db_session: AsyncSession = Depends(get_session),
) -> Union[None, JSONResponse]:
    """タスクを削除.

    指定されたタスク ID のタスクを削除します。

    Args:
        task_id: タスク ID
        db_session: データベースセッション

    Returns:
        204 No Content

    Raises:
        404: タスクが見つかりません
    """
    service = TaskService(db_session)
    try:
        await service.delete_task(task_id, TEST_USER_ID)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
                "message": "タスクが見つかりません",
            },
        )

    return None
