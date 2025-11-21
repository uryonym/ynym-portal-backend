-- FuelRecord（燃費記録）テーブル作成 SQL
-- 日付: 2025-11-19
-- 説明: ユーザーが記録する燃費情報を管理するテーブル

CREATE TABLE IF NOT EXISTS fuel_record (
    -- Primary Key
    id UUID NOT NULL PRIMARY KEY,

    -- Foreign Keys
    vehicle_id UUID NOT NULL,
    user_id UUID NOT NULL,

    -- Core Fields
    refuel_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    total_mileage INTEGER NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    unit_price INTEGER NOT NULL,
    total_cost INTEGER NOT NULL,

    -- Status Fields
    is_full_tank BOOLEAN NOT NULL DEFAULT FALSE,
    gas_station_name VARCHAR(255),

    -- Soft Delete Support
    deleted_at TIMESTAMP WITH TIME ZONE,

    -- Timestamps (JST: UTC+9)
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- インデックス作成（クエリ性能最適化）
CREATE INDEX idx_fuel_record_vehicle_id ON fuel_record(vehicle_id);
CREATE INDEX idx_fuel_record_user_id ON fuel_record(user_id);
CREATE INDEX idx_fuel_record_deleted_at ON fuel_record(deleted_at);
CREATE INDEX idx_fuel_record_created_at ON fuel_record(created_at DESC);
CREATE INDEX idx_fuel_record_refuel_datetime ON fuel_record(refuel_datetime DESC);

-- コメント追加（テーブル説明）
COMMENT ON TABLE fuel_record IS 'ユーザーが記録する燃費情報';
COMMENT ON COLUMN fuel_record.id IS '燃費記録 ID（UUID、主キー）';
COMMENT ON COLUMN fuel_record.vehicle_id IS '車 ID（UUID、外部キー）';
COMMENT ON COLUMN fuel_record.user_id IS 'ユーザー ID（UUID、外部キー）';
COMMENT ON COLUMN fuel_record.refuel_datetime IS '給油日時';
COMMENT ON COLUMN fuel_record.total_mileage IS '総走行距離（km、正の数）';
COMMENT ON COLUMN fuel_record.fuel_type IS '燃料タイプ（例: "ハイオク", "レギュラー", "軽油"）';
COMMENT ON COLUMN fuel_record.unit_price IS '単価（円/L、正の数）';
COMMENT ON COLUMN fuel_record.total_cost IS '総費用（円、0以上の数）';
COMMENT ON COLUMN fuel_record.is_full_tank IS '満タンかどうか';
COMMENT ON COLUMN fuel_record.gas_station_name IS 'ガソリンスタンド名';
COMMENT ON COLUMN fuel_record.deleted_at IS '削除日時（論理削除用）';
COMMENT ON COLUMN fuel_record.created_at IS '作成日時（JST、自動セット）';
COMMENT ON COLUMN fuel_record.updated_at IS '更新日時（JST、自動セット）';
