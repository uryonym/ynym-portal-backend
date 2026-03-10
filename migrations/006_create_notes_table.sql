-- Notes（ノート）テーブル作成 SQL
-- 日付: 2026-02-10
-- 説明: ユーザーが作成するノートを管理するテーブル

CREATE TABLE IF NOT EXISTS notes (
    -- Primary Key
    id UUID NOT NULL PRIMARY KEY,

    -- Foreign Keys
    user_id UUID NOT NULL,
    category_id UUID,

    -- Core Fields
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,

    -- Timestamps (JST: UTC+9)
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- インデックス作成（クエリ性能最適化）
CREATE INDEX idx_notes_user_id ON notes(user_id);
CREATE INDEX idx_notes_category_id ON notes(category_id);
CREATE INDEX idx_notes_user_id_title ON notes(user_id, title);

-- コメント追加（テーブル説明）
COMMENT ON TABLE notes IS 'ユーザーが作成するノート';
COMMENT ON COLUMN notes.id IS 'ノート ID（UUID、主キー）';
COMMENT ON COLUMN notes.user_id IS 'ユーザー ID（UUID、外部キー）';
COMMENT ON COLUMN notes.category_id IS 'カテゴリ ID（UUID、任意）';
COMMENT ON COLUMN notes.title IS 'タイトル（1-255 文字）';
COMMENT ON COLUMN notes.body IS '本文';
COMMENT ON COLUMN notes.created_at IS '作成日時（JST、自動セット）';
COMMENT ON COLUMN notes.updated_at IS '更新日時（JST、自動セット）';
