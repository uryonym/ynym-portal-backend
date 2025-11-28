"""タスク管理サービス層."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import nulls_last
from sqlmodel import col

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.utils.exceptions import NotFoundException


class TaskService:
    """
    タスク管理ビジネスロジック層.

    データベース操作とビジネスロジックを分離し、
    API エンドポイントから使用される。
    """

    def __init__(self, db_session: AsyncSession) -> None:
        """
        TaskService を初期化.

        Args:
            db_session: データベースセッション（依存性注入）
        """
        self.db_session = db_session

    async def list_tasks(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        is_completed: Optional[bool] = None,
    ) -> List[Task]:
        """
        タスク一覧を取得.

        期日が近い順（昇順）でソートされ、期日なしのタスクは
        作成日時の古い順で期日ありのタスクの後に表示される。

        Args:
            user_id: ユーザー ID（将来的に FK として使用）
            skip: スキップするレコード数（ページネーション）
            limit: 取得するレコード数（デフォルト 100、最大 1000）
            is_completed: 完了状態でフィルタ（None: 全件、True: 完了のみ、False: 未完了のみ）

        Returns:
            Task のリスト

        Example:
            >>> service = TaskService(db_session)
            >>> tasks = await service.list_tasks(user_id, skip=0, limit=10)
            >>> incomplete_tasks = await service.list_tasks(user_id, is_completed=False)
        """
        stmt = (
            select(Task)
            .where(col(Task.user_id) == user_id)
            .where(col(Task.deleted_at).is_(None))  # 論理削除フィルター（将来）
        )

        # is_completed フィルタ
        if is_completed is not None:
            stmt = stmt.where(col(Task.is_completed) == is_completed)

        stmt = stmt.order_by(
            nulls_last(asc(col(Task.due_date))),
            asc(col(Task.created_at)),
        ).offset(skip).limit(limit)

        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_task(self, task_id: UUID, user_id: UUID) -> Task:
        """
        タスクを ID で取得.

        Args:
            task_id: タスク ID
            user_id: ユーザー ID（所有権確認用）

        Returns:
            Task オブジェクト

        Raises:
            NotFoundException: タスクが見つからない場合

        Example:
            >>> service = TaskService(db_session)
            >>> task = await service.get_task(task_id, user_id)
        """
        stmt = (
            select(Task)
            .where(col(Task.id) == task_id)
            .where(col(Task.user_id) == user_id)
            .where(col(Task.deleted_at).is_(None))  # 論理削除フィルター（将来）
        )
        result = await self.db_session.execute(stmt)
        task = result.scalars().one_or_none()
        if not task:
            raise NotFoundException(f"タスク ID {task_id} が見つかりません")
        return task

    async def create_task(self, task_create: TaskCreate, user_id: UUID) -> Task:
        """
        新規タスクを作成.

        Args:
            task_create: タスク作成スキーマ
            user_id: タスク所有者のユーザー ID

        Returns:
            作成された Task オブジェクト

        Example:
            >>> service = TaskService(db_session)
            >>> task_data = TaskCreate(title="買い物", description="牛乳を買う")
            >>> task = await service.create_task(task_data, user_id)
        """
        task = Task(
            user_id=user_id,
            title=task_create.title,
            description=task_create.description,
            due_date=task_create.due_date,
            is_completed=task_create.is_completed or False,
        )
        self.db_session.add(task)
        await self.db_session.commit()
        await self.db_session.refresh(task)
        return task

    async def update_task(
        self,
        task_id: UUID,
        task_update: TaskUpdate,
        user_id: UUID,
    ) -> Task:
        """
        既存タスクを更新（部分更新対応）.

        Args:
            task_id: タスク ID
            task_update: タスク更新スキーマ
            user_id: ユーザー ID（所有権確認用）

        Returns:
            更新された Task オブジェクト

        Raises:
            NotFoundException: タスクが見つからない場合

        Example:
            >>> service = TaskService(db_session)
            >>> update_data = TaskUpdate(title="食材の買い物")
            >>> task = await service.update_task(task_id, update_data, user_id)
        """
        task = await self.get_task(task_id, user_id)

        # 更新されたフィールドのみ適用（部分更新）
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        self.db_session.add(task)
        await self.db_session.commit()
        await self.db_session.refresh(task)
        return task

    async def delete_task(self, task_id: UUID, user_id: UUID) -> None:
        """
        タスクを削除（物理削除）.

        Args:
            task_id: タスク ID
            user_id: ユーザー ID（所有権確認用）

        Raises:
            NotFoundException: タスクが見つからない場合

        Example:
            >>> service = TaskService(db_session)
            >>> await service.delete_task(task_id, user_id)
        """
        task = await self.get_task(task_id, user_id)
        await self.db_session.delete(task)
        await self.db_session.commit()
