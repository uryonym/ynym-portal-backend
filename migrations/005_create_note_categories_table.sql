-- NoteCategory（ノートカテゴリ）テーブル作成 SQL
-- 日付: 2026-02-10
-- 説明: ユーザーが作成するノートカテゴリを管理するテーブル

CREATE TABLE IF NOT EXISTS note_categories (
    -- Primary Key
    id UUID NOT NULL PRIMARY KEY,

    -- Foreign Key
    user_id UUID NOT NULL,

    -- Core Fields
    name VARCHAR(255) NOT NULL,

    -- Timestamps (JST: UTC+9)
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- インデックス作成（クエリ性能最適化）
CREATE INDEX idx_note_categories_user_id ON note_categories(user_id);
CREATE INDEX idx_note_categories_user_id_name ON note_categories(user_id, name);

-- コメント追加（テーブル説明）
COMMENT ON TABLE note_categories IS 'ユーザーが作成するノートカテゴリ';
COMMENT ON COLUMN note_categories.id IS 'ノートカテゴリ ID（UUID、主キー）';
COMMENT ON COLUMN note_categories.user_id IS 'ユーザー ID（UUID、外部キー）';
COMMENT ON COLUMN note_categories.name IS 'カテゴリ名（1-255 文字）';
COMMENT ON COLUMN note_categories.created_at IS '作成日時（JST、自動セット）';
COMMENT ON COLUMN note_categories.updated_at IS '更新日時（JST、自動セット）';
