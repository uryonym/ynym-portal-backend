-- FuelRecord（燃費記録）テーブル検証 SQL

SELECT
    table_name,
    column_name,
    data_type,
    is_nullable
FROM
    information_schema.columns
WHERE
    table_name = 'fuel_record'
ORDER BY
    ordinal_position;
