"""タスク管理機能のモデル定義設計書."""

# タスク管理モデル設計 v1.0

## 概要

ynym Portal Backend のタスク管理機能に必要なデータモデルを定義する。
すべてのモデルで UUID (Universally Unique Identifier) をプライマリキーとして採用。
UUID 形式により、分散システム対応・キー衝突の回避・プライバシー保護を実現。

## タイムゾーンの考慮

すべてのタイムスタンプは **日本時間（JST）** で保存される。これはユーザーの所在地がメインに日本であるため。
実装時は `datetime.now(timezone(timedelta(hours=9)))` または JST オブジェクトを使用する。

⚠️ **注意**: 非推奨の `datetime.utcnow()` は使用しない。Python 3.12+ では完全に削除される。

## ID 戦略: UUID の採用

### UUID の特徴

- **グローバルユニーク**: 全世界でユニークな ID 生成が可能
- **分散環境対応**: DB リプリケーション・マイクロサービス対応
- **プライバシー**: シーケンシャル ID と異なり、ID 値から予測・列挙が不可能
- **標準化**: RFC 4122 により業界標準

### 実装方法

- Python 標準ライブラリ `uuid` モジュール使用
- SQLModel での型: `UUID` (Pydantic 対応)
- DB カラム型: PostgreSQL `UUID` 型
- Pydantic スキーマ: 文字列表現で JSON 出力

---

## モデル定義

### 1. User モデル

```python
from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlmodel import SQLModel, Field

# 日本時間（JST）
JST = timezone(timedelta(hours=9))

class User(SQLModel, table=True):
    """ユーザーモデル."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=100)
    email: str = Field(index=True, unique=True, max_length=255)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(JST))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(JST))
```

**フィールド:**

- `id`: UUID (PK)
- `username`: 一意のユーザー名
- `email`: 一意のメールアドレス
- `hashed_password`: bcrypt ハッシュ化パスワード
- `is_active`: アカウント有効フラグ
- `created_at`: 作成日時（日本時間 JST）
- `updated_at`: 更新日時（日本時間 JST）

---

### 2. TaskStatus モデル (マスター)

```python
class TaskStatus(SQLModel, table=True):
    """タスクステータスマスター（管理者定義）."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True, max_length=50)
    label: str = Field(max_length=100)
    order: int = Field(default=0)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(JST))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(JST))
```

**フィールド:**

- `id`: UUID (PK)
- `name`: ステータス識別名 (e.g., "not_started", "in_progress", "completed")
- `label`: 表示用ラベル（日本語）
- `order`: UI 表示順序
- `is_completed`: 完了フラグ（完了状態かどうかの判定）
- `created_at`: 作成日時（日本時間 JST）
- `updated_at`: 更新日時（日本時間 JST）

**デフォルトマスターデータ:**

```
- name: "not_started", label: "未開始", order: 1, is_completed: false
- name: "in_progress", label: "進行中", order: 2, is_completed: false
- name: "completed", label: "完了", order: 3, is_completed: true
- name: "cancelled", label: "キャンセル", order: 4, is_completed: true
```

---

### 3. TaskPriority モデル (マスター)

```python
class TaskPriority(SQLModel, table=True):
    """タスク優先度マスター（管理者定義）."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    level: int = Field(unique=True, ge=1, le=5)
    name: str = Field(max_length=50)
    color_code: str = Field(max_length=7)
    created_at: datetime = Field(default_factory=lambda: datetime.now(JST))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(JST))
```

**フィールド:**

- `id`: UUID (PK)
- `level`: 優先度レベル (1 ～ 5)
- `name`: 優先度名 (e.g., "Low", "Medium", "High")
- `color_code`: HEX カラーコード (e.g., "#808080")
- `created_at`: 作成日時（日本時間 JST）
- `updated_at`: 更新日時（日本時間 JST）

**デフォルトマスターデータ:**

```
- level: 1, name: "Very Low", color_code: "#E0E0E0"
- level: 2, name: "Low", color_code: "#90CAF9"
- level: 3, name: "Medium", color_code: "#FFB74D"
- level: 4, name: "High", color_code: "#EF5350"
- level: 5, name: "Very High", color_code: "#C62828"
```

---

### 4. Task モデル (主体)

```python
class Task(SQLModel, table=True):
    """タスクモデル."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    status_id: UUID = Field(foreign_key="taskstatus.id")
    priority_id: UUID = Field(foreign_key="taskpriority.id")
    due_date: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    order: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(JST))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(JST))
```

**フィールド:**

- `id`: UUID (PK)
- `user_id`: UUID (FK → User.id)
- `title`: タスクタイトル（必須、255 字以内）
- `description`: タスク説明（オプション、2000 字以内）
- `status_id`: UUID (FK → TaskStatus.id)
- `priority_id`: UUID (FK → TaskPriority.id)
- `due_date`: 期限日時（オプション、日本時間 JST）
- `completed_at`: 完了日時（ステータス完了時に自動設定、日本時間 JST）
- `order`: ドラッグ&ドロップ並び替え用順序
- `created_at`: 作成日時（日本時間 JST）
- `updated_at`: 更新日時（日本時間 JST）

**制約:**

- 同一ユーザーでも異なる `order` 値を持つ複数タスク可能
- `status_id` が完了状態の場合、`completed_at` は自動記入

---

### 5. TaskLabel モデル

```python
class TaskLabel(SQLModel, table=True):
    """タスクラベルモデル（ユーザーごと定義可能）."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    name: str = Field(max_length=50)
    color_code: str = Field(max_length=7, default="#808080")
    created_at: datetime = Field(default_factory=lambda: datetime.now(JST))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(JST))

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_label_name"),
    )
```

**フィールド:**

- `id`: UUID (PK)
- `user_id`: UUID (FK → User.id)
- `name`: ラベル名（ユーザーごとユニーク）
- `color_code`: HEX カラーコード
- `created_at`: 作成日時（日本時間 JST）
- `updated_at`: 更新日時（日本時間 JST）

**制約:**

- 同一ユーザー内で同じ名前のラベルは 1 つのみ（複合ユニーク制約）

---

### 6. TaskLabelAssociation モデル (中間テーブル)

```python
class TaskLabelAssociation(SQLModel, table=True):
    """タスクとラベルの多対多関連付け."""

    task_id: UUID = Field(
        foreign_key="task.id",
        primary_key=True,
        index=True
    )
    label_id: UUID = Field(
        foreign_key="tasklabel.id",
        primary_key=True,
        index=True
    )
```

**フィールド:**

- `task_id`: UUID (FK, PK)
- `label_id`: UUID (FK, PK)

**用途:**

- Task と TaskLabel の多対多リレーション実装

---

## Pydantic スキーマ

### TaskCreate スキーマ

```python
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class TaskCreate(BaseModel):
    """タスク作成スキーマ."""

    title: str
    description: Optional[str] = None
    status_id: UUID
    priority_id: UUID
    due_date: Optional[datetime] = None
    label_ids: Optional[list[UUID]] = []
```

### TaskUpdate スキーマ

```python
class TaskUpdate(BaseModel):
    """タスク更新スキーマ."""

    title: Optional[str] = None
    description: Optional[str] = None
    status_id: Optional[UUID] = None
    priority_id: Optional[UUID] = None
    due_date: Optional[datetime] = None
    order: Optional[int] = None
    label_ids: Optional[list[UUID]] = None
```

### TaskResponse スキーマ

```python
class TaskResponse(BaseModel):
    """タスクレスポンススキーマ."""

    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    status_id: UUID
    priority_id: UUID
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    order: int
    created_at: datetime
    updated_at: datetime
```

---

## ER 図（UUID 対応版）

```
┌──────────────────────────┐
│         User             │
├──────────────────────────┤
│ id: UUID (PK)            │
│ username: str (UNIQUE)   │
│ email: str (UNIQUE)      │
│ hashed_password: str     │
│ is_active: bool          │
│ created_at: datetime     │
│ updated_at: datetime     │
└────────────┬─────────────┘
             │ 1:N
             │
    ┌────────▼──────────────────┐
    │        Task               │
    ├───────────────────────────┤
    │ id: UUID (PK)             │
    │ user_id: UUID (FK)        │
    │ title: str                │
    │ description: str          │
    │ status_id: UUID (FK)  ┐   │
    │ priority_id: UUID (FK)├─┐ │
    │ due_date: datetime    │ │ │
    │ completed_at: datetime│ │ │
    │ order: int            │ │ │
    │ created_at: datetime  │ │ │
    │ updated_at: datetime  │ │ │
    └────────┬──────────────┘ │ │
             │                │ │
             │ N:M      ┌──────┘ │
    ┌────────▼──────────┐ N:1   │
    │ TaskLabelAssoc.   │       │
    ├───────────────────┤   ┌───┘
    │ task_id: UUID (FK,PK)│   │
    │ label_id: UUID (FK,PK)   │
    └────────┬───────────┘   │
             │               │
             │ N:M    ┌──────┘
    ┌────────▼──────────────┐ N:1
    │    TaskLabel          │
    ├───────────────────────┤   ┌────────────────┐
    │ id: UUID (PK)         │   │  TaskStatus    │
    │ user_id: UUID (FK)    │   ├────────────────┤
    │ name: str             │   │ id: UUID (PK)  │
    │ color_code: str       │   │ name: str      │
    │ created_at: datetime  │   │ label: str     │
    │ updated_at: datetime  │   │ order: int     │
    └───────────────────────┘   │ is_completed   │
                                └────────────────┘

                                ┌────────────────┐
                                │ TaskPriority   │
                                ├────────────────┤
                                │ id: UUID (PK)  │
                                │ level: int     │
                                │ name: str      │
                                │ color_code: str│
                                └────────────────┘
```

---

## 実装順序

| 優先度 | モデル               | ファイル                      | 依存                     |
| ------ | -------------------- | ----------------------------- | ------------------------ |
| P0     | TaskStatus           | `app/models/task_status.py`   | なし                     |
| P0     | TaskPriority         | `app/models/task_priority.py` | なし                     |
| P1     | Task                 | `app/models/task.py`          | TaskStatus, TaskPriority |
| P2     | TaskLabel            | `app/models/task_label.py`    | User                     |
| P2     | TaskLabelAssociation | `app/models/task_label.py`    | Task, TaskLabel          |
| P0     | スキーマ             | `app/schemas/task.py`         | モデル                   |

---

## 設計原則との適合性

✅ **I. 非同期優先**: SQLModel + asyncpg で完全非同期対応
✅ **II. 型安全性**: 全フィールドに型ヒント、UUID も型安全
✅ **III. TDD**: 実装前にテスト設計
✅ **IV. レイヤー分離**: モデル → スキーマ → サービス → API 層で厳密分離
✅ **V. 品質自動化**: ruff + mypy で UUID 型も検証
✅ **VI. ドキュメント**: 本ドキュメント + docstring で完全記述
✅ **VII. エラーハンドリング**: UUID 形式エラーは ValidationException で処理

---

## PostgreSQL UUID 型対応

PostgreSQL での UUID 型サポート:

```sql
-- UUID 拡張機能の有効化
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- UUID カラム例
CREATE TABLE "user" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ...
);
```

SQLModel + asyncpg での自動対応:

- SQLModel は `UUID` 型を自動的に PostgreSQL `UUID` 型にマッピング
- asyncpg ドライバも UUID 型をネイティブサポート
