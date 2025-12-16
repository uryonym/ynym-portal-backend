-- User テーブル作成 SQL
-- 日付: 2025-12-14
-- 説明: app/models/user.py の User モデルに対応するテーブル

-- UUID 生成関数を利用（既に有効な場合はスキップ）
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT users_email_unique UNIQUE (email)
);
