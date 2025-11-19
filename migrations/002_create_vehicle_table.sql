-- Vehicle（車）テーブル作成 SQL
-- 日付: 2025-11-16
-- 説明: ユーザーが所有する車情報を管理するテーブル

CREATE TABLE IF NOT EXISTS vehicle (
    -- Primary Key
    id UUID NOT NULL PRIMARY KEY,

    -- Foreign Key
    user_id UUID NOT NULL,

    -- Core Fields
    name VARCHAR(255) NOT NULL,
    seq INTEGER NOT NULL,
    maker VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INTEGER,
    number VARCHAR(50),
    tank_capacity FLOAT,

    -- Soft Delete Support
    deleted_at TIMESTAMP WITH TIME ZONE,

    -- Timestamps (JST: UTC+9)
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- インデックス作成（クエリ性能最適化）
CREATE INDEX idx_vehicle_user_id ON vehicle(user_id);
CREATE INDEX idx_vehicle_deleted_at ON vehicle(deleted_at);
CREATE INDEX idx_vehicle_created_at ON vehicle(created_at DESC);

-- コメント追加（テーブル説明）
COMMENT ON TABLE vehicle IS 'ユーザーが所有する車情報';
COMMENT ON COLUMN vehicle.id IS '車 ID（UUID、主キー）';
COMMENT ON COLUMN vehicle.user_id IS 'ユーザー ID（UUID、外部キー）';
COMMENT ON COLUMN vehicle.name IS '車名（1-255 文字）';
COMMENT ON COLUMN vehicle.seq IS 'シーケンス（車の登録順番、正の整数）';
COMMENT ON COLUMN vehicle.maker IS 'メーカー（1-100 文字）';
COMMENT ON COLUMN vehicle.model IS '型式（1-100 文字）';
COMMENT ON COLUMN vehicle.year IS '年式（例: 2023）';
COMMENT ON COLUMN vehicle.number IS 'ナンバー（例: "東京 123あ 1234"、1-50 文字）';
COMMENT ON COLUMN vehicle.tank_capacity IS 'タンク容量（L）';
COMMENT ON COLUMN vehicle.deleted_at IS '削除日時（論理削除用）';
COMMENT ON COLUMN vehicle.created_at IS '作成日時（JST、自動セット）';
COMMENT ON COLUMN vehicle.updated_at IS '更新日時（JST、自動セット）';
