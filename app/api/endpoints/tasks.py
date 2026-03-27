"""タスク関連エンドポイント."""

from typing import Optional, Union
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query, status
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_session
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.security.deps import CurrentUser
from app.services.task_service import TaskService
from app.utils.exceptions import NotFoundException

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _get_task_service(db: Session = Depends(get_session)) -> TaskService:
    return TaskService(TaskRepository(db))


@router.get("", response_model=dict)
def list_tasks(
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_completed: Optional[bool] = Query(None),
    service: TaskService = Depends(_get_task_service),
) -> dict:
    """タスク一覧を取得."""
    tasks = service.list_tasks(
        user_id=current_user.id, skip=skip, limit=limit, is_completed=is_completed
    )
    return {
        "data": [TaskResponse.model_validate(t) for t in tasks],
        "message": "タスク一覧を取得しました",
    }


@router.post("", response_model=None, status_code=status.HTTP_201_CREATED)
def create_task(
    current_user: CurrentUser,
    body: dict = Body(default={}),
    service: TaskService = Depends(_get_task_service),
) -> Union[dict, JSONResponse]:
    """新規タスクを作成."""
    try:
        task_create = TaskCreate(**body)
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "errors": [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()],
                "message": "入力データが正しくありません",
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"errors": [str(e)], "message": "リクエストボディが不正です"},
        )

    created_task = service.create_task(task_create, current_user.id)
    return {
        "data": TaskResponse.model_validate(created_task),
        "message": "タスクが作成されました",
    }


@router.get("/{task_id}", response_model=None)
def get_task(
    current_user: CurrentUser,
    task_id: UUID,
    service: TaskService = Depends(_get_task_service),
) -> Union[dict, JSONResponse]:
    """タスクを取得."""
    try:
        task = service.get_task(task_id, current_user.id)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": str(e), "message": "タスクが見つかりません"},
        )
    return {
        "data": TaskResponse.model_validate(task),
        "message": "タスクが取得されました",
    }


@router.put("/{task_id}", response_model=None)
def update_task(
    current_user: CurrentUser,
    task_id: UUID,
    body: dict = Body(default={}),
    service: TaskService = Depends(_get_task_service),
) -> Union[dict, JSONResponse]:
    """タスクを更新."""
    try:
        task_update = TaskUpdate(**body)
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "errors": [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()],
                "message": "入力データが正しくありません",
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"errors": [str(e)], "message": "リクエストボディが不正です"},
        )

    try:
        updated_task = service.update_task(task_id, task_update, current_user.id)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": str(e), "message": "タスクが見つかりません"},
        )
    return {
        "data": TaskResponse.model_validate(updated_task),
        "message": "タスクが更新されました",
    }


@router.delete("/{task_id}", response_model=None)
def delete_task(
    current_user: CurrentUser,
    task_id: UUID,
    service: TaskService = Depends(_get_task_service),
) -> Union[Response, JSONResponse]:
    """タスクを削除."""
    try:
        service.delete_task(task_id, current_user.id)
    except NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": str(e), "message": "タスクが見つかりません"},
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
