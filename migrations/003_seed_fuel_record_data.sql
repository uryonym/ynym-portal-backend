-- FuelRecord（燃費記録）テーブルテストデータ挿入 SQL
-- 説明: 開発・テスト用のサンプル燃費記録データを作成

INSERT INTO fuel_record (
    id,
    vehicle_id,
    user_id,
    refuel_datetime,
    total_mileage,
    fuel_type,
    unit_price,
    total_cost,
    is_full_tank,
    gas_station_name,
    deleted_at,
    created_at,
    updated_at
)
VALUES
    (
        '650e8400-e29b-41d4-a716-446655440001'::UUID,
        '550e8400-e29b-41d4-a716-446655440001'::UUID,
        '550e8400-e29b-41d4-a716-446655440000'::UUID,
        '2025-11-19 10:00:00+09:00'::TIMESTAMP WITH TIME ZONE,
        10000,
        'ハイオク',
        165,
        6600,
        TRUE,
        'ENEOS 東京駅前',
        NULL,
        NOW(),
        NOW()
    ),
    (
        '650e8400-e29b-41d4-a716-446655440002'::UUID,
        '550e8400-e29b-41d4-a716-446655440001'::UUID,
        '550e8400-e29b-41d4-a716-446655440000'::UUID,
        '2025-11-18 15:30:00+09:00'::TIMESTAMP WITH TIME ZONE,
        10100,
        'ハイオク',
        164,
        6400,
        FALSE,
        'JOMO 神宮前',
        NULL,
        NOW(),
        NOW()
    ),
    (
        '650e8400-e29b-41d4-a716-446655440003'::UUID,
        '550e8400-e29b-41d4-a716-446655440002'::UUID,
        '550e8400-e29b-41d4-a716-446655440000'::UUID,
        '2025-11-17 08:00:00+09:00'::TIMESTAMP WITH TIME ZONE,
        5500,
        'レギュラー',
        160,
        3200,
        TRUE,
        'shell 渋谷',
        NULL,
        NOW(),
        NOW()
    );
