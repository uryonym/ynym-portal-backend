"""TaskService.list_tasks() のユニットテスト."""

import pytest
from uuid import UUID
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.task import Task
from app.services.task_service import TaskService

# 日本標準時 (JST)
JST = ZoneInfo("Asia/Tokyo")

# テスト用ユーザー ID（固定値）
TEST_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")


class TestTaskServiceListTasks:
    """TaskService.list_tasks() のテストケース."""

    @pytest.fixture
    async def test_db_session(self):
        """テスト用非同期データベースセッション."""
        # インメモリ SQLite でテスト
        engine = create_async_engine("sqlite+aiosqlite:///:memory:")

        # テーブルを作成
        from app.models.base import TimestampModel
        async with engine.begin() as conn:
            await conn.run_sync(TimestampModel.metadata.create_all)

        # セッションファクトリ
        AsyncSessionFactory = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

        async with AsyncSessionFactory() as session:
            yield session

    async def test_list_tasks_empty(self, test_db_session: AsyncSession) -> None:
        """タスクが存在しない場合、空リストを返す."""
        service = TaskService(test_db_session)
        tasks = await service.list_tasks(TEST_USER_ID)
        assert tasks == []

    async def test_list_tasks_single_task(self, test_db_session: AsyncSession) -> None:
        """1 つのタスクが存在する場合、そのタスクを返す."""
        service = TaskService(test_db_session)

        # テストデータ作成
        task = Task(
            user_id=TEST_USER_ID,
            title="テストタスク",
            description="テスト用の説明",
        )
        test_db_session.add(task)
        await test_db_session.commit()

        # list_tasks() で取得
        tasks = await service.list_tasks(TEST_USER_ID)
        assert len(tasks) == 1
        assert tasks[0].title == "テストタスク"

    async def test_list_tasks_sorting_by_due_date(self, test_db_session: AsyncSession) -> None:
        """タスクが期日昇順でソートされる."""
        service = TaskService(test_db_session)

        today = date.today()

        # 3 つのタスクを異なる期日で作成
        task1 = Task(
            user_id=TEST_USER_ID,
            title="タスク3（最新期日）",
            due_date=today + timedelta(days=5),
        )
        task2 = Task(
            user_id=TEST_USER_ID,
            title="タスク1（最初の期日）",
            due_date=today + timedelta(days=1),
        )
        task3 = Task(
            user_id=TEST_USER_ID,
            title="タスク2（中間期日）",
            due_date=today + timedelta(days=3),
        )

        test_db_session.add_all([task1, task2, task3])
        await test_db_session.commit()

        # ソート順序を確認
        tasks = await service.list_tasks(TEST_USER_ID)
        assert len(tasks) == 3
        assert tasks[0].title == "タスク1（最初の期日）"
        assert tasks[1].title == "タスク2（中間期日）"
        assert tasks[2].title == "タスク3（最新期日）"

    async def test_list_tasks_undated_tasks_at_end(self, test_db_session: AsyncSession) -> None:
        """期日なしのタスクは期日ありのタスク後に表示される."""
        service = TaskService(test_db_session)

        today = date.today()

        # 期日ありタスク
        task_with_due = Task(
            user_id=TEST_USER_ID,
            title="期日ありタスク",
            due_date=today + timedelta(days=5),
        )

        # 期日なしタスク
        task_without_due = Task(
            user_id=TEST_USER_ID,
            title="期日なしタスク",
            due_date=None,
        )

        test_db_session.add_all([task_without_due, task_with_due])
        await test_db_session.commit()

        # ソート順序を確認（期日ありが最初、期日なしが後）
        tasks = await service.list_tasks(TEST_USER_ID)
        assert len(tasks) == 2
        assert tasks[0].title == "期日ありタスク"
        assert tasks[1].title == "期日なしタスク"

    async def test_list_tasks_pagination_skip(self, test_db_session: AsyncSession) -> None:
        """skip パラメータでレコードをスキップ."""
        service = TaskService(test_db_session)

        # 5 つのタスクを作成
        for i in range(5):
            task = Task(
                user_id=TEST_USER_ID,
                title=f"タスク{i+1}",
            )
            test_db_session.add(task)
        await test_db_session.commit()

        # skip=2, limit=2 で取得
        tasks = await service.list_tasks(TEST_USER_ID, skip=2, limit=2)
        assert len(tasks) == 2

    async def test_list_tasks_pagination_limit(self, test_db_session: AsyncSession) -> None:
        """limit パラメータで取得数を制限."""
        service = TaskService(test_db_session)

        # 10 つのタスクを作成
        for i in range(10):
            task = Task(
                user_id=TEST_USER_ID,
                title=f"タスク{i+1}",
            )
            test_db_session.add(task)
        await test_db_session.commit()

        # limit=5 で取得
        tasks = await service.list_tasks(TEST_USER_ID, skip=0, limit=5)
        assert len(tasks) == 5

    async def test_list_tasks_filters_by_user_id(self, test_db_session: AsyncSession) -> None:
        """指定したユーザー ID のタスクのみ返す."""
        service = TaskService(test_db_session)

        other_user_id = UUID("550e8400-e29b-41d4-a716-446655440001")

        # 異なるユーザーでタスク作成
        task1 = Task(
            user_id=TEST_USER_ID,
            title="ユーザー1のタスク",
        )
        task2 = Task(
            user_id=other_user_id,
            title="ユーザー2のタスク",
        )

        test_db_session.add_all([task1, task2])
        await test_db_session.commit()

        # TEST_USER_ID のタスクのみ取得
        tasks = await service.list_tasks(TEST_USER_ID)
        assert len(tasks) == 1
        assert tasks[0].title == "ユーザー1のタスク"

    async def test_list_tasks_created_at_sorting_for_same_due_date(
        self, test_db_session: AsyncSession
    ) -> None:
        """同じ期日のタスクは created_at でソート."""
        service = TaskService(test_db_session)

        today = date.today()
        now = datetime.now(JST)

        # 同じ期日で複数タスク作成（作成時刻が異なる）
        task1 = Task(
            user_id=TEST_USER_ID,
            title="最初のタスク",
            due_date=today + timedelta(days=1),
            created_at=now,
        )

        task2 = Task(
            user_id=TEST_USER_ID,
            title="次のタスク",
            due_date=today + timedelta(days=1),
            created_at=now + timedelta(seconds=1),
        )

        test_db_session.add_all([task2, task1])
        await test_db_session.commit()

        # created_at 順でソートされることを確認
        tasks = await service.list_tasks(TEST_USER_ID)
        assert len(tasks) == 2
        assert tasks[0].title == "最初のタスク"
        assert tasks[1].title == "次のタスク"
