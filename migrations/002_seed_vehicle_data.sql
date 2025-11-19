-- Vehicle テーブルテストデータ插入 SQL
-- 説明: 開発・テスト用のサンプル車データを作成

INSERT INTO vehicle (
    id,
    user_id,
    name,
    seq,
    maker,
    model,
    year,
    number,
    tank_capacity,
    deleted_at,
    created_at,
    updated_at
)
VALUES
    (
        '550e8400-e29b-41d4-a716-446655440001'::UUID,
        '550e8400-e29b-41d4-a716-446655440000'::UUID,
        'マイカー1',
        1,
        'Toyota',
        'Prius',
        2023,
        '東京 123あ 1234',
        50.0,
        NULL,
        NOW(),
        NOW()
    ),
    (
        '550e8400-e29b-41d4-a716-446655440002'::UUID,
        '550e8400-e29b-41d4-a716-446655440000'::UUID,
        'マイカー2',
        2,
        'Honda',
        'Fit',
        2021,
        '神奈川 456い 5678',
        40.0,
        NULL,
        NOW(),
        NOW()
    ),
    (
        '550e8400-e29b-41d4-a716-446655440003'::UUID,
        '550e8400-e29b-41d4-a716-446655440000'::UUID,
        'マイカー3',
        3,
        'Nissan',
        'Note',
        2020,
        '埼玉 789う 9012',
        42.0,
        NULL,
        NOW(),
        NOW()
    );
