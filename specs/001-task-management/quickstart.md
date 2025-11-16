# Quick Start: Task Management Implementation

**Date**: 2025-11-12
**Phase**: Phase 1 - Design & Contracts
**Purpose**: タスク管理機能の実装を開始するための最初のステップガイド

---

## Overview

このガイドは、実装チームがタスク管理機能の開発を始めるためのステップ・バイ・ステップ手順です。

**成果物**:

- Task SQLModel （`app/models/task.py`）
- Task Pydantic スキーマ （`app/schemas/task.py`）
- Task サービス層 （`app/services/task_service.py`）
- Task API エンドポイント （`app/api/endpoints/tasks.py`）
- ユニット・統合テスト

**期間**: 約 2-3 日（チーム規模・経験に応じて）

---

## Prerequisites

### 環境確認

```bash
# Python バージョン
python --version  # 3.12+ 必須

# 依存パッケージ確認
pip list | grep -E "fastapi|sqlmodel|pytest"

# 開発ツール確認
mypy --version
ruff --version
black --version
```

### リポジトリの準備

```bash
# 作業ブランチを確認
git branch -a | grep 001-task-management

# ブランチ切り替え（存在しない場合は作成）
git checkout 001-task-management || git checkout -b 001-task-management

# 最新の仕様書を確認
cat specs/001-task-management/spec.md
cat specs/001-task-management/data-model.md
cat specs/001-task-management/contracts/task_api.openapi.yaml
```

---

## Step 1: SQLModel 定義（app/models/task.py）

### 実装ターゲット

- Task クラスを定義（base.py の UUIDModel を継承）
- フィールド定義：title, description, due_date, is_completed, completed_at, order, deleted_at
- Timestamp: created_at, updated_at は UUIDModel から自動継承

### コード実装例

```python
# app/models/task.py
"""タスクモデル定義."""

from datetime import date, datetime
from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field
from app.models.base import UUIDModel  # Base class with UUID PK + JST timestamps

class Task(UUIDModel, table=True):
    """タスクモデル."""

    __tablename__ = "task"

    user_id: UUID = Field(index=True, description="ユーザー ID")
    title: str = Field(max_length=255, description="タスクタイトル")
    description: Optional[str] = Field(default=None, max_length=2000, description="詳細")
    is_completed: bool = Field(default=False, description="完了状態")
    completed_at: Optional[datetime] = Field(default=None, description="完了日時")
    due_date: Optional[date] = Field(default=None, index=True, description="期日")
    order: int = Field(default=0, ge=0, description="順序")
    deleted_at: Optional[datetime] = Field(default=None, index=True, description="削除日時")
```

### 確認チェック

- [ ] ファイルが `app/models/task.py` に作成されている
- [ ] `mypy app/models/task.py` でエラーなし
- [ ] `ruff check app/models/task.py` でエラーなし

---

## Step 2: Pydantic スキーマ定義（app/schemas/task.py）

### 実装ターゲット

- TaskCreate: POST リクエスト用（title 必須、その他オプション）
- TaskUpdate: PUT リクエスト用（すべてオプション）
- TaskResponse: レスポンス用（id, user_id, created_at, updated_at 含む）

### コード実装例

```python
# app/schemas/task.py
"""タスク Pydantic スキーマ."""

from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class TaskCreate(BaseModel):
    """タスク作成スキーマ."""
    title: str = Field(..., min_length=1, max_length=255, description="タイトル")
    description: Optional[str] = Field(default=None, max_length=2000)
    due_date: Optional[date] = Field(default=None)

class TaskUpdate(BaseModel):
    """タスク更新スキーマ."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_completed: Optional[bool] = Field(default=None)
    due_date: Optional[date] = Field(default=None)

class TaskResponse(BaseModel):
    """タスクレスポンススキーマ."""
    model_config = ConfigDict(from_attributes=True)  # ORM mode

    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    is_completed: bool
    completed_at: Optional[datetime]
    due_date: Optional[date]
    order: int
    created_at: datetime
    updated_at: datetime
```

### 確認チェック

- [ ] ファイルが `app/schemas/task.py` に作成されている
- [ ] `mypy app/schemas/task.py` でエラーなし
- [ ] `ruff check app/schemas/task.py` でエラーなし

---

## Step 3: サービス層（app/services/task_service.py）

### 実装ターゲット

- `list_tasks(user_id, skip, limit)` - タスク一覧取得（ソート付き）
- `create_task(user_id, task_create)` - タスク作成
- `get_task(task_id, user_id)` - タスク詳細取得
- `update_task(task_id, user_id, task_update)` - タスク更新
- `delete_task(task_id, user_id)` - タスク削除

### コード実装例

```python
# app/services/task_service.py
"""タスク管理ビジネスロジック."""

from datetime import datetime, timezone, timedelta
from typing import Optional
from uuid import UUID
from sqlalchemy import select, nulls_last
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.utils.exceptions import NotFoundException, ValidationException

JST = timezone(timedelta(hours=9))

class TaskService:
    """タスク管理サービス."""

    @staticmethod
    async def list_tasks(
        session: AsyncSession,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[TaskResponse]:
        """タスク一覧取得（期日ソート + 作成日時フォールバック）."""
        query = (
            select(Task)
            .where(Task.user_id == user_id)
            .where(Task.deleted_at.is_(None))
            .order_by(nulls_last(Task.due_date.asc()), Task.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        tasks = result.scalars().all()
        return [TaskResponse.model_validate(task) for task in tasks]

    @staticmethod
    async def create_task(
        session: AsyncSession,
        user_id: UUID,
        task_create: TaskCreate,
    ) -> TaskResponse:
        """タスク作成."""
        task = Task(
            user_id=user_id,
            title=task_create.title,
            description=task_create.description,
            due_date=task_create.due_date,
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return TaskResponse.model_validate(task)

    @staticmethod
    async def get_task(
        session: AsyncSession,
        task_id: UUID,
        user_id: UUID,
    ) -> TaskResponse:
        """タスク詳細取得."""
        task = await session.get(Task, task_id)
        if not task or task.user_id != user_id or task.deleted_at is not None:
            raise NotFoundException("タスクが見つかりません")
        return TaskResponse.model_validate(task)

    @staticmethod
    async def update_task(
        session: AsyncSession,
        task_id: UUID,
        user_id: UUID,
        task_update: TaskUpdate,
    ) -> TaskResponse:
        """タスク更新."""
        task = await session.get(Task, task_id)
        if not task or task.user_id != user_id or task.deleted_at is not None:
            raise NotFoundException("タスクが見つかりません")

        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description
        if task_update.is_completed is not None:
            task.is_completed = task_update.is_completed
            if task_update.is_completed:
                task.completed_at = datetime.now(JST)
            else:
                task.completed_at = None
        if task_update.due_date is not None:
            task.due_date = task_update.due_date

        await session.commit()
        await session.refresh(task)
        return TaskResponse.model_validate(task)

    @staticmethod
    async def delete_task(
        session: AsyncSession,
        task_id: UUID,
        user_id: UUID,
    ) -> None:
        """タスク削除（物理削除）."""
        task = await session.get(Task, task_id)
        if not task or task.user_id != user_id or task.deleted_at is not None:
            raise NotFoundException("タスクが見つかりません")

        await session.delete(task)
        await session.commit()
```

### 確認チェック

- [ ] ファイルが `app/services/task_service.py` に作成されている
- [ ] 全メソッドで非同期実装（async/await）
- [ ] `mypy app/services/task_service.py` でエラーなし
- [ ] `ruff check app/services/task_service.py` でエラーなし

---

## Step 4: API エンドポイント（app/api/endpoints/tasks.py）

### 実装ターゲット

- `GET /tasks` - タスク一覧
- `POST /tasks` - タスク作成
- `GET /tasks/{task_id}` - タスク詳細
- `PUT /tasks/{task_id}` - タスク更新
- `DELETE /tasks/{task_id}` - タスク削除

### コード実装例

```python
# app/api/endpoints/tasks.py
"""タスク管理 API エンドポイント."""

from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import get_session
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService
from app.utils.exceptions import NotFoundException

router = APIRouter(prefix="/tasks", tags=["tasks"])

# テスト用固定ユーザー ID（認証実装後に Depends に変更）
TEST_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")

@router.get("", response_model=dict)
async def list_tasks(
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> dict:
    """タスク一覧取得."""
    tasks = await TaskService.list_tasks(session, TEST_USER_ID, skip, limit)
    return {"data": tasks, "message": "タスク一覧を取得しました"}

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """タスク作成."""
    task = await TaskService.create_task(session, TEST_USER_ID, task_create)
    return {"data": task, "message": "タスクが作成されました"}

@router.get("/{task_id}", response_model=dict)
async def get_task(
    task_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """タスク詳細取得."""
    try:
        task = await TaskService.get_task(session, task_id, TEST_USER_ID)
        return {"data": task, "message": "タスクを取得しました"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{task_id}", response_model=dict)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """タスク更新."""
    try:
        task = await TaskService.update_task(session, task_id, TEST_USER_ID, task_update)
        return {"data": task, "message": "タスクが更新されました"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> None:
    """タスク削除."""
    try:
        await TaskService.delete_task(session, task_id, TEST_USER_ID)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
```

### ルータ登録

`app/api/router.py` に以下を追加：

```python
from app.api.endpoints import tasks

router.include_router(tasks.router)
```

### 確認チェック

- [ ] ファイルが `app/api/endpoints/tasks.py` に作成されている
- [ ] ルータが `app/api/router.py` に登録されている
- [ ] `mypy app/api/endpoints/tasks.py` でエラーなし
- [ ] `ruff check app/api/endpoints/tasks.py` でエラーなし

---

## Step 5: テスト実装

### ユニットテスト（tests/unit/test_task_service.py）

```python
# tests/unit/test_task_service.py
"""タスクサービスのユニットテスト."""

import pytest
from uuid import uuid4
from datetime import date
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.task import Task
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate
from app.utils.exceptions import NotFoundException

@pytest.mark.asyncio
async def test_create_task(session: AsyncSession):
    """タスク作成のテスト."""
    user_id = uuid4()
    task_create = TaskCreate(
        title="テストタスク",
        description="テスト説明",
        due_date=date(2025, 11, 15),
    )

    task = await TaskService.create_task(session, user_id, task_create)

    assert task.title == "テストタスク"
    assert task.user_id == user_id
    assert task.is_completed is False
```

### 統合テスト（tests/integration/test_task_endpoints.py）

```python
# tests/integration/test_task_endpoints.py
"""タスク API エンドポイント統合テスト."""

import pytest
from httpx import AsyncClient
from fastapi import FastAPI

@pytest.mark.asyncio
async def test_list_tasks(client: AsyncClient):
    """タスク一覧取得 API テスト."""
    response = await client.get("/tasks")
    assert response.status_code == 200
    assert "data" in response.json()
```

### 確認チェック

- [ ] テストファイルが作成されている
- [ ] テスト実行: `pytest tests/unit/test_task_service.py -v`
- [ ] テスト実行: `pytest tests/integration/test_task_endpoints.py -v`
- [ ] カバレッジ確認: `pytest --cov=app tests/`

---

## Step 6: 動作確認

### ローカルサーバー起動

```bash
# 開発サーバー起動
python -m uvicorn app.main:app --reload

# ブラウザで確認
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

### cURL でテスト

```bash
# タスク一覧取得
curl -X GET "http://localhost:8000/tasks"

# タスク作成
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title":"買い物","due_date":"2025-11-15"}'

# タスク更新
curl -X PUT "http://localhost:8000/tasks/{task_id}" \
  -H "Content-Type: application/json" \
  -d '{"is_completed":true}'

# タスク削除
curl -X DELETE "http://localhost:8000/tasks/{task_id}"
```

---

## Step 7: コード品質チェック

```bash
# 型チェック
mypy app/

# Linting
ruff check app/

# フォーマット
black app/

# テスト + カバレッジ
pytest tests/ --cov=app --cov-report=html
```

---

## Troubleshooting

### ImportError: No module named 'app.models.base'

→ `app/models/base.py` が存在し、`UUIDModel` が定義されているか確認

### TypeError: Expected 'SessionMaker' instance

→ `get_session()` 依存関数が `app/database.py` に定義されているか確認

### ValidationError: title must be string

→ Pydantic スキーマの型定義を確認（`TaskCreate.title` は `str` 型）

---

## Next Steps

1. ✅ ステップ 1-7 が完了したら、GitHub PR を作成
2. コードレビューを実施
3. CI/CD パイプラインで自動テスト実行
4. マージ後、`/speckit.tasks` コマンドで実装タスク一覧を生成
5. 計画フェーズを終了し、実装フェーズへ移行

---

## Reference Documents

- **Specification**: [spec.md](spec.md)
- **Data Model**: [data-model.md](data-model.md)
- **API Contracts**: [contracts/task_api.openapi.yaml](contracts/task_api.openapi.yaml)
- **Constitution**: [`.specify/memory/constitution.md`](.specify/memory/constitution.md)
- **Base Model**: [`app/models/base.py`](../../app/models/base.py)
