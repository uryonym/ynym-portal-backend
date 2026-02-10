-- NoteCategory（ノートカテゴリ）テーブル検証 SQL

SELECT
    table_name,
    column_name,
    data_type,
    is_nullable
FROM
    information_schema.columns
WHERE
    table_name = 'note_categories'
ORDER BY
    ordinal_position;
