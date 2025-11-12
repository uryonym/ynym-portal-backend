# タスク実装計画: タスク管理

**ブランチ**: `001-task-management`
**日付**: 2025-11-12
**仕様書**: [spec.md](spec.md)
**データモデル**: [data-model.md](data-model.md)
**API コントラクト**: [contracts/task_api.openapi.yaml](contracts/task_api.openapi.yaml)

---

## 概要

このドキュメントは、タスク管理機能を実装するための具体的なタスク一覧です。各タスクは独立して実行可能で、LLM が自動的に完了できるように設計されています。

### 実装戦略

- **MVP スコープ**: Phase 1 (セットアップ) + Phase 2 (基礎) + User Story 1 & 2 (P1 ストーリー)
- **段階的デリバリー**: User Story 3 & 4 (P2 ストーリー) は Phase 3 以降
- **テスト**:ユニット + 統合テスト
- **品質ゲート**: ruff (lint), mypy (型チェック), pytest (テスト実行)

### 統計

| カテゴリ                    | 数  |
| --------------------------- | --- |
| 総タスク数                  | 49  |
| Phase 1 (セットアップ)      | 5   |
| Phase 2 (基礎)              | 8   |
| Phase 3 (User Story 1 - P1) | 12  |
| Phase 4 (User Story 2 - P1) | 12  |
| Phase 5 (User Story 3 - P2) | 8   |
| Phase 6 (User Story 4 - P2) | 2   |
| Phase 7 (ポーランド & 品質) | 2   |

### 並列実行可能性

- **Phase 1**: 順序実行必須（初期化）
- **Phase 2**: 順序実行必須（全ストーリー共有）
- **Phase 3 & 4**: 並列実行可能（独立したストーリー）
- **Phase 5 & 6**: 並列実行可能（Phase 3 & 4 完了後）
- **Phase 7**: すべてのフェーズ完了後

---

## Phase 1: セットアップ

**目的**: プロジェクト初期化、ディレクトリ構造、基本設定

### タスク

- [x] T001 プロジェクト構造確認：`app/models/`、`app/schemas/`、`app/services/`、`app/api/endpoints/`、`tests/unit/`、`tests/integration/` が存在することを確認
- [x] T002 PostgreSQL データベースの接続確認：`app/database.py` を確認し、asyncpg ドライバが設定されていることを確認
- [x] T003 FastAPI ルータ登録：`app/api/router.py` にタスクエンドポイント用ルータ登録スポットがあることを確認
- [x] T004 テスト環境セットアップ：`pytest.ini` または `pyproject.toml` で pytest-asyncio がインストールされていることを確認、`conftest.py` でデータベーステストフィクスチャ確認
- [x] T005 開発用スクリプト準備：`cd app && python -m pytest ../tests/` でテスト実行可能なことを確認、`ruff check .` と `mypy app/` でクリーンアップ可能なことを確認

---

## Phase 2: 基礎 (全ストーリー共有)

**目的**: Task モデル、基本スキーマ、サービス層基盤

### タスク

- [x] T006 [P] Task SQLModel 作成：`app/models/task.py` に Task クラスを作成。UUIDModel を継承。フィールド：`user_id`, `title`, `description`, `is_completed`, `completed_at`, `due_date`, `order`, `deleted_at`。型ヒント完備、Docstring 記載
- [x] T007 [P] Task スキーマ作成：`app/schemas/task.py` に TaskCreate、TaskUpdate、TaskResponse スキーマを作成。Pydantic v2 で `field_validator` を使用。title 1-255 文字、description 0-2000 文字の検証実装
- [x] T008 [P] TaskService ベース層：`app/services/task_service.py` に TaskService クラス作成。`__init__(self, db_session: AsyncSession)` で DI 可能。ソート実装：`order_by(nulls_last(Task.due_date.asc()), Task.created_at.asc())`
- [x] T009 base.py の確認：`app/models/base.py` が JST (UTC+9) タイムスタンプを正しく使用しているか確認。`datetime.now(JST)` で `created_at`、`updated_at` が自動セットされることを確認
- [x] T010 例外クラス確認：`app/utils/exceptions.py` に `ValidationException`、`NotFoundException` が定義されていることを確認
- [x] T011 [P] ユニットテスト基盤：`tests/unit/test_task_schemas.py` でスキーマバリデーション（タイトル空、タイトル超過文字数、説明超過文字数）のテストケース作成。26 個のテストケース（TaskCreate: 11、TaskUpdate: 11、EdgeCases: 4）で全テスト合格 ✅
- [x] T012 [P] 統合テスト基盤：`tests/integration/test_task_endpoints.py` で API エンドポイント統合テストの骨組み作成。データベーステストフィクスチャ確認。19 個のテストメソッド（GET /tasks、POST /tasks、GET /{id}、PUT /{id}、DELETE /{id}）を含む ✅
- [x] T013 データベースマイグレーション：手動 DDL SQL で Task テーブルを PostgreSQL に作成。`migrations/001_create_task_table.sql` を作成。全カラム（id, user_id, title, description, is_completed, completed_at, due_date, order, deleted_at, created_at, updated_at）、インデックス（user_id, due_date, deleted_at）、制約を実装。関連ファイル: README.md（実行手順）、rollback SQL、seed SQL、verify SQL ✅

---

## Phase 3: User Story 1 - すべてのタスクを表示（優先度: P1）

**ゴール**: ユーザーがタスク管理画面にアクセスしてすべてのタスクを一覧表示で確認できる

**独立テスト基準**:

- [ ] GET /tasks エンドポイントが存在し、201 ステータスで JSON 配列を返す
- [ ] 複数のタスクが期日昇順（最も近い期日が最初）でソートされて返される
- [ ] 期日なしのタスクは作成日時昇順で期日ありのタスク後に返される
- [ ] 空のタスクリストの場合、空配列が返される
- [ ] 各タスクレスポンスは TaskResponse スキーマに準拠

### タスク

- [x] T014 [P] [US1] TaskService.list_tasks() 実装：`app/services/task_service.py` に `async def list_tasks(skip: int = 0, limit: int = 100) -> List[Task]` メソッド追加。SQLAlchemy `nulls_last()` でソート実装。skip/limit パラメータでページネーション対応、user_id フィルタで属するタスクのみ取得 ✅
- [x] T015 [P] [US1] ユニットテスト - リスト取得：`tests/unit/test_task_service.py` で `test_list_tasks_empty`、`test_list_tasks_with_multiple_tasks`、`test_list_tasks_sorting_by_due_date`、`test_list_tasks_undated_tasks_at_end` テストケース作成。4/4 テスト合格 ✅
- [x] T016 [P] [US1] GET /tasks エンドポイント実装：`app/api/endpoints/tasks.py` に `@router.get("/tasks")` エンドポイント作成。クエリパラメータ：skip (default 0), limit (default 100, max 1000)。レスポンス：`{ "data": [TaskResponse], "message": "タスク一覧を取得しました" }` ✅
- [x] T017 [US1] エンドポイント登録：`app/api/router.py` に tasks ルータを登録。`from app.api.endpoints import tasks` → `app.include_router(tasks.router)` ✅
- [x] T018 [US1] 統合テスト - GET /tasks：`tests/integration/test_task_endpoints.py` に `test_get_tasks_list_empty`、`test_get_tasks_list_with_tasks`、`test_get_tasks_sorting_correct` テスト追加。3/3 テスト合格 ✅
- [x] T019 [US1] コード品質：`ruff check app/api/endpoints/tasks.py` と `mypy app/api/endpoints/tasks.py` でエラーなし ✅
- [x] T020 [US1] タスク作成テスト用フィクスチャ：`tests/conftest.py` に Task テストデータ作成用 fixture 追加。3 つのタスク（期日あり、期日なし、完了済み）を作成 ✅
- [x] T021 [US1] ローカルテスト実行：`pytest tests/integration/test_task_endpoints.py::test_get_tasks_list_with_tasks -v` でテスト実行、パス確認 ✅
- [x] T022 [US1] API ドキュメント：`docs/api/endpoints.md` に GET /tasks エンドポイント説明追加。期日ソート仕様を記載 ✅
- [x] T023 [US1] 完了チェック：すべての US1 タスク完了後、`pytest tests/ -k US1` でテスト実行、100% パス確認（35/35 テスト合格） ✅
- [x] T024 [US1] コミット：`git add -A && git commit -m "feat: Task list endpoint (US1 - Display all tasks)"` ✅

---

## Phase 4: User Story 2 - モーダルで新規タスクを作成（優先度: P1）

**ゴール**: ユーザーが追加ボタンを押してモーダルを開き、タスク情報を入力して新規タスクを作成できる

**独立テスト基準**:

- [ ] POST /tasks エンドポイントが存在し、201 ステータスで作成したタスクの TaskResponse を返す
- [ ] 必須フィールド（title）が空の場合、400 ステータスと検証エラーメッセージが返される
- [ ] 作成されたタスクはデータベースに永続化される
- [ ] 作成されたタスクの created_at と updated_at は現在の JST 時刻に自動セットされる

### タスク

- [x] T025 [P] [US2] TaskService.create_task() 実装：`app/services/task_service.py` に `async def create_task(task_create: TaskCreate, user_id: UUID) -> Task` メソッド追加。user_id を固定値（`550e8400-e29b-41d4-a716-446655440000`）で設定（後続認証実装で変更） ✅
- [ ] T026 [P] [US2] ユニットテスト - 作成成功：`tests/unit/test_task_service.py` に `test_create_task_success`、`test_create_task_with_all_fields` テスト追加
- [ ] T027 [P] [US2] ユニットテスト - 作成エラー：`tests/unit/test_task_service.py` に `test_create_task_title_empty_fails`、`test_create_task_title_exceeds_max_length_fails`、`test_create_task_description_exceeds_max_length_fails` テスト追加
- [ ] T028 [P] [US2] POST /tasks エンドポイント実装：`app/api/endpoints/tasks.py` に `@router.post("/tasks")` エンドポイント作成。リクエスト: TaskCreate、レスポンス: `{ "data": TaskResponse, "message": "タスクが作成されました" }` (201 status code)
- [ ] T029 [US2] エラーハンドリング：POST /tasks で ValidationException キャッチして 400 ステータス + エラー詳細返却。メッセージ例：`"title は必須項目です"`, `"title は 255 文字以内である必要があります"`
- [ ] T030 [US2] 統合テスト - POST /tasks 成功：`tests/integration/test_task_endpoints.py` に `test_post_tasks_create_success`、`test_post_tasks_create_with_all_fields` テスト追加
- [ ] T031 [US2] 統合テスト - POST /tasks エラー：`tests/integration/test_task_endpoints.py` に `test_post_tasks_missing_title_fails`、`test_post_tasks_title_too_long_fails` テスト追加
- [ ] T032 [US2] Timestamp 検証：作成されたタスクの created_at, updated_at が現在の JST 時刻か確認するテスト追加
- [ ] T033 [US2] コード品質：`ruff check app/api/endpoints/tasks.py` と `mypy app/services/task_service.py` でエラーなし
- [ ] T034 [US2] ローカルテスト実行：`pytest tests/integration/test_task_endpoints.py::test_post_tasks_create_success -v` でテスト実行、パス確認
- [ ] T035 [US2] API ドキュメント：`docs/api/endpoints.md` に POST /tasks エンドポイント説明追加。リクエストスキーマ例、レスポンス例、エラーレスポンス例を記載
- [ ] T036 [US2] 完了チェック：`pytest tests/ -k US2` でテスト実行、100% パス確認
- [ ] T037 [US2] コミット：`git add -A && git commit -m "feat: Create task endpoint (US2 - Create task via modal)"`

---

## Phase 5: User Story 3 - 既存タスクを編集（優先度: P2）

**ゴール**: ユーザーがタスク一覧からタスクをタップして、そのタスクの内容を編集できる

**独立テスト基準**:

- [ ] PUT /tasks/{task_id} エンドポイントが存在し、200 ステータスで更新後のタスク情報を返す
- [ ] タスクが存在しない場合、404 ステータスとエラーメッセージが返される
- [ ] 更新後のタスクの updated_at は現在の JST 時刻に更新される
- [ ] 更新対象のフィールド（title など）が正しく更新される

### タスク

- [ ] T038 [P] [US3] TaskService.get_task() 実装：`app/services/task_service.py` に `async def get_task(task_id: UUID) -> Task` メソッド追加。NotFoundException を発生させて 404 対応
- [ ] T039 [P] [US3] TaskService.update_task() 実装：`app/services/task_service.py` に `async def update_task(task_id: UUID, task_update: TaskUpdate) -> Task` メソッド追加。部分更新対応（指定されたフィールドのみ更新）。updated_at 自動更新
- [ ] T040 [P] [US3] ユニットテスト - 取得・更新：`tests/unit/test_task_service.py` に `test_get_task_success`、`test_get_task_not_found_fails`、`test_update_task_success`、`test_update_task_partial` テスト追加
- [ ] T041 [US3] GET /tasks/{task_id} エンドポイント実装：`app/api/endpoints/tasks.py` に `@router.get("/tasks/{task_id}")` エンドポイント作成。レスポンス: TaskResponse、404 時エラーメッセージ
- [ ] T042 [US3] PUT /tasks/{task_id} エンドポイント実装：`app/api/endpoints/tasks.py` に `@router.put("/tasks/{task_id}")` エンドポイント作成。リクエスト: TaskUpdate、レスポンス: `{ "data": TaskResponse, "message": "タスクが更新されました" }` (200 status code)
- [ ] T043 [US3] 統合テスト - GET /tasks/{task_id}：`tests/integration/test_task_endpoints.py` に `test_get_task_by_id_success`、`test_get_task_by_id_not_found` テスト追加
- [ ] T044 [US3] 統合テスト - PUT /tasks/{task_id}：`tests/integration/test_task_endpoints.py` に `test_put_tasks_update_success`、`test_put_tasks_partial_update`、`test_put_tasks_not_found_fails` テスト追加
- [ ] T045 [US3] コード品質：`ruff check` + `mypy` でエラーなし
- [ ] T046 [US3] ローカルテスト実行：`pytest tests/ -k US3 -v` でテスト実行、パス確認

---

## Phase 6: User Story 4 - タスクを削除（優先度: P2）

**ゴール**: ユーザーが不要なタスクを削除できる

**独立テスト基準**:

- [ ] DELETE /tasks/{task_id} エンドポイントが存在し、204 ステータス（No Content）で削除完了を返す
- [ ] タスクが存在しない場合、404 ステータスとエラーメッセージが返される
- [ ] 削除後、GET /tasks/{task_id} は 404 を返す

### タスク

- [ ] T047 [P] [US4] TaskService.delete_task() 実装：`app/services/task_service.py` に `async def delete_task(task_id: UUID) -> None` メソッド追加。NotFoundException 発生時 404 対応。物理削除実装
- [ ] T048 [US4] DELETE /tasks/{task_id} エンドポイント実装：`app/api/endpoints/tasks.py` に `@router.delete("/tasks/{task_id}")` エンドポイント作成。レスポンス: 204 No Content
- [ ] T049 [US4] 統合テスト - DELETE：`tests/integration/test_task_endpoints.py` に `test_delete_task_success`、`test_delete_task_not_found_fails` テスト追加

---

## Phase 7: ポーランド & 品質ゲート

**目的**: コード品質、ドキュメント、最終検証

### タスク

- [ ] T050 [P] 全体品質チェック：`ruff check app/` (0 errors)、`mypy app/` (strict mode 0 errors)、`black --check app/`（フォーマッティング）実行
- [ ] T051 全体テスト実行：`pytest tests/ -v --cov=app --cov-report=term-missing` でカバレッジ確認。目標：80% 以上

---

## 依存関係グラフ

```
Phase 1 (Setup) → Phase 2 (Foundation) → {Phase 3 (US1) ∥ Phase 4 (US2)} → {Phase 5 (US3) ∥ Phase 6 (US4)} → Phase 7 (Polish)
```

### 並列実行パターン

#### MVP 完成までの最短経路（3-4 日）

1. **Day 1**: Phase 1 + Phase 2 完了
2. **Day 2**: Phase 3 (US1) + Phase 4 (US2) 並列実行
3. **Day 3**: Phase 7 (品質) 実行、デプロイ準備

#### フルスコープ完成までの経路（5-6 日）

1. **Day 1**: Phase 1 + Phase 2 完了
2. **Day 2-3**: Phase 3 (US1) + Phase 4 (US2) 並列実行
3. **Day 4**: Phase 5 (US3) + Phase 6 (US4) 並列実行
4. **Day 5**: Phase 7 (品質) 実行

---

## 実装ガイド

### タスク実行の流れ

1. **前提条件チェック**: 各タスクの `[ ] T00X` をクリアするまで次に進まない
2. **独立実行**: [P] マークされたタスクは任意の順序で並列実行可能
3. **テスト駆動**: 各実装タスクの直後にテストタスク実行
4. **品質ゲート**: Phase 7 前に ruff, mypy, pytest で 100% クリア

### コード例：TaskService の構造

```python
# app/services/task_service.py
from sqlmodel import select
from sqlalchemy import nulls_last

class TaskService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def list_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """タスク一覧取得（期日昇順、期日なしは作成日時昇順）."""
        stmt = (
            select(Task)
            .order_by(nulls_last(Task.due_date.asc()), Task.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def create_task(self, task_create: TaskCreate, user_id: UUID) -> Task:
        """新規タスク作成."""
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

    async def get_task(self, task_id: UUID) -> Task:
        """タスク取得（存在しない場合は NotFoundException）."""
        stmt = select(Task).where(Task.id == task_id)
        result = await self.db_session.execute(stmt)
        task = result.scalars().one_or_none()
        if not task:
            raise NotFoundException(f"Task {task_id} not found")
        return task

    async def update_task(self, task_id: UUID, task_update: TaskUpdate) -> Task:
        """タスク更新（部分更新対応）."""
        task = await self.get_task(task_id)
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        task.updated_at = datetime.now(JST)  # 更新日時を現在時刻に設定
        self.db_session.add(task)
        await self.db_session.commit()
        await self.db_session.refresh(task)
        return task

    async def delete_task(self, task_id: UUID) -> None:
        """タスク削除（物理削除）."""
        task = await self.get_task(task_id)
        await self.db_session.delete(task)
        await self.db_session.commit()
```

### コード例：エンドポイント構造

```python
# app/api/endpoints/tasks.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("")
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """タスク一覧取得."""
    service = TaskService(db)
    tasks = await service.list_tasks(skip, limit)
    return {"data": tasks, "message": "タスク一覧を取得しました"}

@router.post("")
async def create_task(
    task_create: TaskCreate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """新規タスク作成."""
    try:
        service = TaskService(db)
        user_id = UUID("550e8400-e29b-41d4-a716-446655440000")  # テスト用固定 ID
        task = await service.create_task(task_create, user_id)
        return {"data": task, "message": "タスクが作成されました"}
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{task_id}")
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """タスク取得."""
    try:
        service = TaskService(db)
        task = await service.get_task(task_id)
        return {"data": task, "message": "タスク情報を取得しました"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{task_id}")
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """タスク更新."""
    try:
        service = TaskService(db)
        task = await service.update_task(task_id, task_update)
        return {"data": task, "message": "タスクが更新されました"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{task_id}")
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """タスク削除."""
    try:
        service = TaskService(db)
        await service.delete_task(task_id)
        return None  # 204 No Content
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
```

---

## 推奨リソース

- [FastAPI 公式ドキュメント](https://fastapi.tiangolo.com/)
- [SQLModel 公式ドキュメント](https://sqlmodel.tiangolo.com/)
- [Pydantic v2 マイグレーション](https://docs.pydantic.dev/latest/migration/)
- [pytest-asyncio ドキュメント](https://pytest-asyncio.readthedocs.io/)

---

## チェックリスト

### Phase 1-2 完了後

- [ ] プロジェクト構造確認
- [ ] データベース接続確認
- [ ] テスト環境動作確認
- [ ] Task モデル作成完了
- [ ] TaskService ベース実装完了

### MVP (US1+US2) 完了後

- [ ] GET /tasks エンドポイント完全動作
- [ ] POST /tasks エンドポイント完全動作
- [ ] すべての US1, US2 テスト 100% パス
- [ ] ruff, mypy エラーなし

### フルスコープ完了後

- [ ] 全 4 User Story 実装完了
- [ ] 全テスト 100% パス
- [ ] 全 49 タスク完了
- [ ] コード品質ゲート 100% クリア
- [ ] デプロイ準備完了

---

**最終更新**: 2025-11-12
**バージョン**: 1.0
**ステータス**: 実行準備完了
