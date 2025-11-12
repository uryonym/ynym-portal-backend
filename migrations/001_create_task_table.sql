-- Task Management Migration
-- ファイル: migrations/001_create_task_table.sql
-- 説明: Task テーブルの作成
-- 実行日: 2025-11-12
-- 手動実行: psql -U postgres -d ynym_portal_dev -f migrations/001_create_task_table.sql

-- UUID 型の拡張を有効化（既に有効な場合はスキップ）
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Task テーブルを作成
CREATE TABLE IF NOT EXISTS "task" (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Foreign Key (将来の User テーブル参照)
    user_id UUID NOT NULL,

    -- Core Fields
    title VARCHAR(255) NOT NULL,
    description TEXT,

    -- Status Fields
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,

    -- Deadline
    due_date DATE,

    -- Ordering
    "order" INTEGER NOT NULL DEFAULT 0 CHECK ("order" >= 0),

    -- Soft Delete Support
    deleted_at TIMESTAMP WITH TIME ZONE,

    -- Timestamps (JST: UTC+9)
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT title_not_empty CHECK (LENGTH(TRIM(title)) > 0),
    CONSTRAINT description_not_too_long CHECK (LENGTH(description) <= 2000)
);

-- インデックスを作成
-- ユーザー ID でのフィルタ/JOINを高速化
CREATE INDEX IF NOT EXISTS idx_task_user_id ON "task"(user_id);

-- 期日でのソート/フィルタを高速化
CREATE INDEX IF NOT EXISTS idx_task_due_date ON "task"(due_date);

-- 論理削除対応（将来）: deleted_at が NULL のタスクを高速に取得
CREATE INDEX IF NOT EXISTS idx_task_deleted_at ON "task"(deleted_at);

-- テーブル作成完了を確認
SELECT
    table_name,
    column_name,
    data_type,
    is_nullable
FROM
    information_schema.columns
WHERE
    table_name = 'task'
ORDER BY
    ordinal_position;
