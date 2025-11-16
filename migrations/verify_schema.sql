-- Task Table Schema Verification
-- ファイル: migrations/verify_schema.sql
-- 説明: Task テーブルのスキーマを検証

-- 1. テーブル存在確認
SELECT
    CASE
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'task')
        THEN '✓ Task テーブルが存在します'
        ELSE '✗ Task テーブルが見つかりません'
    END AS table_check;

-- 2. カラム定義確認
\echo '\n--- Task テーブルのカラム定義 ---'
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM
    information_schema.columns
WHERE
    table_name = 'task'
ORDER BY
    ordinal_position;

-- 3. プライマリキー確認
\echo '\n--- プライマリキー ---'
SELECT
    a.attname AS column_name,
    t.typname AS data_type
FROM
    pg_index i
    JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
    JOIN pg_type t ON a.atttypid = t.oid
WHERE
    i.indrelid = 'task'::regclass
    AND i.indisprimary;

-- 4. インデックス一覧
\echo '\n--- インデックス ---'
SELECT
    indexname,
    indexdef
FROM
    pg_indexes
WHERE
    tablename = 'task'
ORDER BY
    indexname;

-- 5. 制約一覧
\echo '\n--- テーブル制約 ---'
SELECT
    constraint_name,
    constraint_type,
    check_clause
FROM
    information_schema.table_constraints
    LEFT JOIN information_schema.check_constraints USING (constraint_name)
WHERE
    table_name = 'task'
ORDER BY
    constraint_name;

-- 6. テーブルサイズ
\echo '\n--- テーブルサイズ ---'
SELECT
    pg_size_pretty(pg_total_relation_size('task')) AS total_size,
    pg_size_pretty(pg_relation_size('task')) AS table_size,
    pg_size_pretty(pg_total_relation_size('task') - pg_relation_size('task')) AS indexes_size;

-- 7. レコード数
\echo '\n--- レコード数 ---'
SELECT
    COUNT(*) AS total_records,
    SUM(CASE WHEN is_completed = TRUE THEN 1 ELSE 0 END) AS completed_count,
    SUM(CASE WHEN is_completed = FALSE THEN 1 ELSE 0 END) AS incomplete_count,
    SUM(CASE WHEN due_date IS NOT NULL THEN 1 ELSE 0 END) AS with_due_date_count,
    SUM(CASE WHEN deleted_at IS NOT NULL THEN 1 ELSE 0 END) AS deleted_count
FROM "task";

\echo '\n✓ スキーマ検証完了'
