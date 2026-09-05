"""タスク管理サービス層."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.models.base import JST
from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate
from app.utils.exceptions import NotFoundException


class TaskService:
    """タスク管理ビジネスロジック層."""

    def __init__(self, task_repo: TaskRepository) -> None:
        self.task_repo = task_repo

    def list_tasks(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        is_completed: Optional[bool] = None,
    ) -> List[Task]:
        """タスク一覧を取得（期日昇順、期日なしは末尾）."""
        return self.task_repo.list_by_user(user_id, skip, limit, is_completed)

    def get_task(self, task_id: UUID, user_id: UUID) -> Task:
        """タスクを ID で取得.

        Raises:
            NotFoundException: タスクが存在しない場合
        """
        task = self.task_repo.get_by_id_and_user(task_id, user_id)
        if not task:
            raise NotFoundException(f"タスク ID {task_id} が見つかりません")
        return task

    def create_task(self, task_create: TaskCreate, user_id: UUID) -> Task:
        """新規タスクを作成."""
        task = Task(
            user_id=user_id,
            title=task_create.title,
            description=task_create.description,
            due_date=task_create.due_date,
            is_completed=task_create.is_completed or False,
        )
        return self.task_repo.save(task)

    def update_task(
        self, task_id: UUID, task_update: TaskUpdate, user_id: UUID
    ) -> Task:
        """既存タスクを部分更新.

        is_completed を True に変更した場合、completed_at を自動設定する。
        """
        task = self.get_task(task_id, user_id)
        update_data = task_update.model_dump(exclude_unset=True)

        if "is_completed" in update_data:
            if update_data["is_completed"] and not task.is_completed:
                update_data["completed_at"] = datetime.now(JST)
            elif not update_data["is_completed"] and task.is_completed:
                update_data["completed_at"] = None

        for field, value in update_data.items():
            setattr(task, field, value)

        return self.task_repo.save(task)

    def delete_task(self, task_id: UUID, user_id: UUID) -> None:
        """タスクを物理削除."""
        task = self.get_task(task_id, user_id)
        self.task_repo.delete(task)
