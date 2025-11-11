# Data Model Design: Task Management

**Date**: 2025-11-12
**Phase**: Phase 1 - Design & Contracts
**Purpose**: Task 管理機能のデータモデルを設計・定義

## Entity: Task

### Conceptual Model

ユーザーのタスク管理用エンティティ。複数のタスクをリスト化し、作成・更新・削除・ソートできる。

### SQLModel クラス定義

```python
# app/models/task.py

from datetime import date, datetime
from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field
from app.models.base import UUIDModel  # Base class with UUID PK + timestamps

class Task(UUIDModel, table=True):
    """
    タスクモデル.

    ユーザーが作成・管理するタスクを表現する。
    """

    __tablename__ = "task"

    # Foreign Keys
    user_id: UUID = Field(
        index=True,
        description="タスク所有ユーザーの UUID（将来 FK 制約追加予定）",
    )

    # Core Fields
    title: str = Field(
        max_length=255,
        index=False,
        description="タスクのタイトル（必須、255 字以内）",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="タスクの詳細説明（オプション、2000 字以内）",
    )

    # Status Fields
    is_completed: bool = Field(
        default=False,
        description="完了状態フラグ（True=完了、False=未完了）",
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        description="タスク完了日時（日本時間 JST）",
    )

    # Deadline
    due_date: Optional[date] = Field(
        default=None,
        index=True,
        description="タスク期日（オプション、YYYY-MM-DD 形式）",
    )

    # Ordering
    order: int = Field(
        default=0,
        ge=0,
        description="ドラッグ&ドロップ用表示順序（将来の UI ソート対応）",
    )

    # Soft Delete Support (Future)
    deleted_at: Optional[datetime] = Field(
        default=None,
        index=True,
        description="論理削除日時（初期バージョンは未使用、将来対応）",
    )

    # Timestamps inherited from UUIDModel
    # - id: UUID (PK, auto-generated)
    # - created_at: datetime (日本時間 JST, auto-generated)
    # - updated_at: datetime (日本時間 JST, auto-set on update)
```

### Field Specifications

| フィールド     | 型        | 制約               | 説明                            |
| -------------- | --------- | ------------------ | ------------------------------- |
| `id`           | UUID      | PK, Auto           | UUID プライマリキー（RFC 4122） |
| `user_id`      | UUID      | Required, Index    | タスク所有者 UID                |
| `title`        | str       | Required, Max 255  | タスクタイトル                  |
| `description`  | str?      | Optional, Max 2000 | タスク詳細                      |
| `is_completed` | bool      | Default: False     | 完了フラグ                      |
| `completed_at` | datetime? | Optional           | 完了日時（JST）                 |
| `due_date`     | date?     | Optional, Index    | 期日（日付のみ）                |
| `order`        | int       | Default: 0, >= 0   | ソート用序数                    |
| `deleted_at`   | datetime? | Optional, Index    | 論理削除日時（将来）            |
| `created_at`   | datetime  | Auto               | 作成日時（JST）                 |
| `updated_at`   | datetime  | Auto               | 更新日時（JST）                 |

### Key Design Decisions

1. **UUID Primary Key**: グローバルユニークで分散対応
2. **date vs datetime**: 期日は日付のみ（ユーザーは日単位のタスク管理が一般的）
3. **`is_completed` + `completed_at`**: 完了状態を 2 フィールドで管理（一貫性維持）
4. **`deleted_at`**: 初期バージョンは物理削除するが、ディレクトリ構造は論理削除対応
5. **`order` 序数**: 将来のドラッグ&ドロップ並び替え機能に対応
6. **Timestamps (JST)**: プロジェクト全体で日本時間統一（app/models/base.py 参照）

### Relationships

**Task → User** (将来実装)

```
Task.user_id -> User.id (1:N)
```

- 現在は FK 制約なし（User テーブル実装後に追加）
- テスト/シード では固定 UUID を使用

### Validation Rules

- `title`: 1 字以上 255 字以下（空文字列不可）
- `description`: 0 字以上 2000 字以下
- `due_date`: 過去日付も許可（ユーザーが修正可能）
- `order`: >= 0（負の値不可）
- `is_completed + completed_at` の整合性:
  - `is_completed = True` → `completed_at` は NULL または現在日時
  - `is_completed = False` → `completed_at` は NULL（推奨）

### Indexes

- `id` (PK)
- `user_id` (FK lookup/filter)
- `due_date` (sort performance)
- `deleted_at` (soft delete filter、将来)

---

## Query Patterns

### Get All Tasks (with sorting)

```python
from sqlalchemy import nulls_last, select
from app.models.task import Task

# 期日の昇順（期日なしは最後）→ 作成日時の昇順
query = (
    select(Task)
    .where(Task.user_id == user_id)
    .where(Task.deleted_at.is_(None))  # 論理削除フィルター（将来）
    .order_by(
        nulls_last(Task.due_date.asc()),
        Task.created_at.asc()
    )
)
```

### Create Task

```python
new_task = Task(
    user_id=user_id,
    title="買い物",
    description="牛乳を買う",
    due_date=date(2025, 11, 15),
    is_completed=False,
)
session.add(new_task)
await session.commit()
await session.refresh(new_task)
```

### Update Task

```python
task.title = "食材の買い物"
task.due_date = date(2025, 11, 20)
task.updated_at = datetime.now(JST)  # 自動セット（BaseModel で処理）
await session.commit()
```

### Mark as Completed

```python
task.is_completed = True
task.completed_at = datetime.now(JST)
await session.commit()
```

### Delete Task (Physical)

```python
await session.delete(task)
await session.commit()
```

### Delete Task (Logical, Future)

```python
task.deleted_at = datetime.now(JST)
await session.commit()
```

---

## Schema: Pydantic Validation

### TaskCreate (POST リクエスト用)

```python
# app/schemas/task.py

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    """タスク作成スキーマ."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="タスクタイトル（必須）",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="タスク詳細（オプション）",
    )
    due_date: Optional[date] = Field(
        default=None,
        description="期日（オプション、YYYY-MM-DD）",
    )
```

### TaskUpdate (PUT リクエスト用)

```python
class TaskUpdate(BaseModel):
    """タスク更新スキーマ."""

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="タスクタイトル（オプション）",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="タスク詳細（オプション）",
    )
    is_completed: Optional[bool] = Field(
        default=None,
        description="完了状態（オプション）",
    )
    due_date: Optional[date] = Field(
        default=None,
        description="期日（オプション、YYYY-MM-DD）",
    )
```

### TaskResponse (レスポンス用)

```python
from uuid import UUID
from datetime import datetime

class TaskResponse(BaseModel):
    """タスクレスポンススキーマ."""

    model_config = ConfigDict(from_attributes=True)  # ORM mode

    id: UUID = Field(description="タスク ID")
    user_id: UUID = Field(description="所有者 UID")
    title: str = Field(description="タスクタイトル")
    description: Optional[str] = Field(description="タスク詳細")
    is_completed: bool = Field(description="完了状態")
    completed_at: Optional[datetime] = Field(description="完了日時（ISO 8601）")
    due_date: Optional[date] = Field(description="期日（YYYY-MM-DD）")
    order: int = Field(description="表示順序")
    created_at: datetime = Field(description="作成日時（ISO 8601）")
    updated_at: datetime = Field(description="更新日時（ISO 8601）")
```

---

## ER Diagram

```
┌────────────────────────────────────────┐
│            Task                        │
├────────────────────────────────────────┤
│ id: UUID (PK)                          │
│ user_id: UUID (Index)                  │
│ title: str (255)                       │
│ description: str (2000, NULL)          │
│ is_completed: bool                     │
│ completed_at: datetime (NULL)          │
│ due_date: date (Index, NULL)           │
│ order: int (>= 0)                      │
│ deleted_at: datetime (Index, NULL)     │
│ created_at: datetime (JST)             │
│ updated_at: datetime (JST)             │
└────────────────────────────────────────┘
         ↓ (1:N)
┌────────────────────────────────────────┐
│            User (Future)               │
├────────────────────────────────────────┤
│ id: UUID (PK)                          │
│ username: str (UNIQUE)                 │
│ email: str (UNIQUE)                    │
│ ...                                    │
└────────────────────────────────────────┘
```

---

## Database Migration Notes

### Initial Schema (Alembic will manage)

```sql
CREATE TABLE "task" (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(2000),
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    due_date DATE,
    "order" INTEGER NOT NULL DEFAULT 0 CHECK ("order" >= 0),
    deleted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE INDEX idx_task_user_id ON "task" (user_id);
CREATE INDEX idx_task_due_date ON "task" (due_date);
CREATE INDEX idx_task_deleted_at ON "task" (deleted_at);
```

---

## Summary

- **Single Entity**: Task のみ（ユーザーテーブルは後続）
- **UUID-based**: RFC 4122 準拠
- **JST Timestamps**: タイムゾーン統一
- **Soft Delete Ready**: `deleted_at` 対応ディレクトリ構造
- **Future-proof**: FK、ドラッグ&ドロップ、マルチユーザー対応可能
