-- task_listsの列順変更

-- テーブルのバックアップ
SELECT * INTO task_lists_20240419
FROM task_lists;

-- テーブルの削除
DROP TABLE task_lists;

-- テーブルの作成
CREATE TABLE task_lists (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying NOT NULL,
    seq integer NOT NULL,
    uid character varying NOT NULL,
    created_at timestamp(6) without time zone NOT NULL,
    updated_at timestamp(6) without time zone NOT NULL
);
ALTER TABLE ONLY task_lists ADD CONSTRAINT task_lists_pkey PRIMARY KEY (id);
CREATE UNIQUE INDEX index_task_lists_on_seq_and_uid ON task_lists USING btree (seq, uid);

-- データの戻し
INSERT INTO task_lists
SELECT
  id,
  name,
  seq,
  uid,
  created_at,
  updated_at
FROM task_lists_20240419;

-- バックアップテーブルの削除
DROP TABLE task_lists_20240419;
