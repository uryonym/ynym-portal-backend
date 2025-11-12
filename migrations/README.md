# データベースマイグレーション実行ガイド

**プロジェクト**: ynym Portal Backend
**日付**: 2025-11-12
**バージョン**: Phase 2 T013

## マイグレーションファイル一覧

### 001_create_task_table.sql

**目的**: Task テーブルの作成
**内容**:

- UUID 型拡張の有効化
- Task テーブル定義（11 カラム）
- インデックス作成（3 個）
- 制約定義（4 個）

## 前提条件

### 必要なもの

1. **PostgreSQL サーバー** (バージョン 12.0 以上)

   - 実行確認: `psql --version`

2. **データベース接続情報**

   - Host: `localhost` (またはリモートホスト)
   - Port: `5432` (デフォルト)
   - User: `postgres` (またはスーパーユーザー)
   - Database: `ynym_portal_dev` (テスト用) / `ynym_portal_prod` (本番用)

3. **接続確認**
   ```bash
   psql -h localhost -U postgres -d ynym_portal_dev -c "SELECT 1"
   ```

## マイグレーション実行方法

### 方法 1: psql コマンドで直接実行（推奨）

```bash
# テスト環境
psql -h localhost -U postgres -d ynym_portal_dev -f migrations/001_create_task_table.sql

# または .env ファイルから接続情報を読み込む
export DATABASE_URL="postgresql://postgres@localhost/ynym_portal_dev"
psql "$DATABASE_URL" -f migrations/001_create_task_table.sql
```

### 方法 2: Python スクリプトから実行

```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

async def run_migration():
    engine = create_async_engine("postgresql+asyncpg://postgres@localhost/ynym_portal_dev")

    async with engine.begin() as conn:
        # SQL ファイルを読み込み
        with open("migrations/001_create_task_table.sql") as f:
            sql = f.read()

        # 実行
        await conn.run_sync(conn.connection.exec_driver_sql, sql)

asyncio.run(run_migration())
```

### 方法 3: Docker コンテナで実行

```bash
# PostgreSQL コンテナが起動している場合
docker exec -i postgres-container psql -U postgres -d ynym_portal_dev < migrations/001_create_task_table.sql
```

## マイグレーション検証

### テーブル作成確認

```sql
-- Task テーブルが存在することを確認
SELECT table_name FROM information_schema.tables
WHERE table_name = 'task';

-- カラム一覧を確認
\d task

-- インデックス一覧を確認
SELECT indexname FROM pg_indexes WHERE tablename = 'task';
```

### Python で確認

```python
import asyncio
from sqlalchemy import text, inspect
from app.database import engine

async def verify_migration():
    async with engine.begin() as conn:
        inspector = inspect(engine.sync_engine)
        tables = inspector.get_table_names()
        print(f"Tables: {tables}")

        if 'task' in tables:
            columns = inspector.get_columns('task')
            print("Task table columns:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")

asyncio.run(verify_migration())
```

## ロールバック（テーブル削除）

**警告**: このコマンドはすべてのデータを削除します

```sql
DROP TABLE IF EXISTS "task" CASCADE;
```

または

```bash
psql -h localhost -U postgres -d ynym_portal_dev -c "DROP TABLE IF EXISTS \"task\" CASCADE;"
```

## トラブルシューティング

### エラー: `ERROR: relation "task" already exists`

**原因**: Task テーブルが既に存在している
**解決策**:

```sql
-- 既存テーブルを確認
\d task

-- 必要に応じて削除してから再実行
DROP TABLE IF EXISTS "task" CASCADE;
```

### エラー: `ERROR: permission denied for schema public`

**原因**: ユーザーに SCHEMA 権限がない
**解決策**: スーパーユーザー (postgres) で実行

### エラー: `ERROR: connection refused`

**原因**: PostgreSQL サーバーが起動していない
**解決策**:

```bash
# Linux/macOS
brew services start postgresql

# Docker
docker start postgres-container
```

## マイグレーション履歴管理

### バージョン管理（Git）

```bash
# マイグレーションファイルをコミット
git add migrations/001_create_task_table.sql
git commit -m "database: Create task table (T013)"
```

### 実行ログの記録（推奨）

```bash
# マイグレーション実行ログを記録
psql -h localhost -U postgres -d ynym_portal_dev -f migrations/001_create_task_table.sql \
  | tee migrations/execution_logs/001_execution_2025-11-12.log
```

## Phase 2 T013 チェックリスト

- [ ] SQL ファイルを確認: `migrations/001_create_task_table.sql`
- [ ] PostgreSQL が起動していることを確認
- [ ] マイグレーション前: `SELECT count(*) FROM information_schema.tables WHERE table_name='task'`
- [ ] マイグレーション実行: `psql -f migrations/001_create_task_table.sql`
- [ ] マイグレーション後: `\d task` でテーブル構造を確認
- [ ] インデックス確認: `SELECT indexname FROM pg_indexes WHERE tablename='task'`
- [ ] テストデータ挿入（オプション）: `INSERT INTO task (user_id, title) VALUES (...)`
- [ ] 統合テスト実行: `pytest tests/integration/ -v`

## 関連ファイル

- **モデル定義**: `app/models/task.py`
- **スキーマ定義**: `app/schemas/task.py`
- **データモデルドキュメント**: `specs/001-task-management/data-model.md`
- **統合テスト**: `tests/integration/test_task_endpoints.py`
