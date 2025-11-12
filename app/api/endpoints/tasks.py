"""Task 関連エンドポイント."""

from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.task import Task
from app.schemas.task import TaskResponse
from app.services.task_service import TaskService

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
            created_at=task.created_at or datetime.now(),
            updated_at=task.updated_at or datetime.now(),
        )
        for task in tasks
    ]

    return {
        "data": task_responses,
        "message": "タスク一覧を取得しました",
    }
