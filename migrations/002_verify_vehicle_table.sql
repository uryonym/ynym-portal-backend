-- Vehicle テーブル作成の検証 SQL
-- 説明: vehicle テーブルが正しく作成されたことを確認

-- テーブルの存在確認
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public' AND table_name = 'vehicle';

-- テーブルカラムの確認
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'vehicle'
ORDER BY ordinal_position;

-- インデックスの確認
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public' AND tablename = 'vehicle';

-- テーブルサイズの確認
SELECT
    table_name,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public' AND table_name = 'vehicle';
