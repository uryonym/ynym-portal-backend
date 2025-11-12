-- Rollback Migration: Drop Task Table
-- ファイル: migrations/rollback_001_create_task_table.sql
-- 説明: Task テーブルの削除（T013 ロールバック用）
-- 警告: このスクリプトはすべてのデータを削除します

-- インデックスを削除（カスケード）
DROP INDEX IF EXISTS idx_task_deleted_at CASCADE;
DROP INDEX IF EXISTS idx_task_due_date CASCADE;
DROP INDEX IF EXISTS idx_task_user_id CASCADE;

-- Task テーブルを削除
DROP TABLE IF EXISTS "task" CASCADE;

-- テーブル削除確認
SELECT
    CASE
        WHEN COUNT(*) = 0 THEN 'Task テーブルが正常に削除されました'
        ELSE 'エラー: Task テーブルがまだ存在します'
    END AS result
FROM
    information_schema.tables
WHERE
    table_name = 'task';
