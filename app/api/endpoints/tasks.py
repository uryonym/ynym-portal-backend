"""Task 関連エンドポイント."""

from datetime import datetime, timedelta, timezone
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import TaskService

# 日本時間（JST）のタイムゾーン設定
JST = timezone(timedelta(hours=9))

router = APIRouter(prefix="/tasks", tags=["tasks"])

# テスト用の固定ユーザー ID（後続認証実装で JWT から取得）
TEST_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")


@router.get("", response_model=dict)
async def list_tasks(
    skip: int = Query(0, ge=0, description="スキップするレコード数"),
    limit: int = Query(100, ge=1, le=1000, description="取得するレコード数"),
    db_session: AsyncSession = Depends(get_session),
) -> dict:
    """タスク一覧を取得.

    期日が近い順（昇順）でソートされ、期日なしのタスクは
    作成日時の古い順で期日ありのタスクの後に表示されます。

    Args:
        skip: スキップするレコード数（デフォルト 0）
        limit: 取得するレコード数（デフォルト 100、最大 1000）
        db_session: データベースセッション

    Returns:
        {
            "data": [TaskResponse, ...],
            "message": "タスク一覧を取得しました"
        }
    """
    service = TaskService(db_session)
    tasks: List[Task] = await service.list_tasks(
        user_id=TEST_USER_ID, skip=skip, limit=limit
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


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    db_session: AsyncSession = Depends(get_session),
) -> dict:
    """新規タスクを作成.

    リクエスト本体に TaskCreate スキーマで指定されたタスク情報を使用して
    新規タスクを作成します。作成されたタスクはレスポンス本体に返されます。

    Args:
        task_create: タスク作成スキーマ
        db_session: データベースセッション

    Returns:
        {
            "data": TaskResponse,
            "message": "タスクが作成されました"
        }
    """
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
