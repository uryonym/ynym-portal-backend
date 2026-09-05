"""タスクリポジトリ."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import asc, select
from sqlalchemy.sql import nulls_last

from app.models.task import Task
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """タスクに関するデータアクセスを担う."""

    def __init__(self, session) -> None:
        super().__init__(session, Task)

    def list_by_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        is_completed: Optional[bool] = None,
    ) -> List[Task]:
        """ユーザーのタスク一覧を取得（期日昇順、期日なしは末尾）."""
        stmt = (
            select(Task)
            .where(Task.user_id == user_id)
            .where(Task.deleted_at.is_(None))
        )
        if is_completed is not None:
            stmt = stmt.where(Task.is_completed == is_completed)
        stmt = (
            stmt.order_by(
                nulls_last(asc(Task.due_date)),
                asc(Task.created_at),
            )
            .offset(skip)
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_by_id_and_user(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """task_id と user_id でタスクを取得（所有権確認）."""
        stmt = (
            select(Task)
            .where(Task.id == task_id)
            .where(Task.user_id == user_id)
            .where(Task.deleted_at.is_(None))
        )
        return self.session.execute(stmt).scalars().one_or_none()
