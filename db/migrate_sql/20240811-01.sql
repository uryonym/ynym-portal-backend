-- task_listsテーブルの削除
DROP TABLE task_lists;


-- taksからtask_list_id列の削除

-- テーブルのバックアップ
SELECT * INTO tasks_20240811
FROM tasks;

-- テーブルの削除
DROP TABLE tasks;

-- テーブルの作成
CREATE TABLE tasks (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    title character varying NOT NULL,
    description character varying,
    dead_line date,
    is_complete boolean DEFAULT false NOT NULL,
    uid character varying NOT NULL,
    created_at timestamp(6) without time zone NOT NULL,
    updated_at timestamp(6) without time zone NOT NULL
);
ALTER TABLE ONLY tasks ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);

-- データの戻し
INSERT INTO tasks
SELECT
  id,
  title,
  description,
  dead_line,
  is_complete,
  uid,
  created_at,
  updated_at
FROM tasks_20240811;

-- バックアップテーブルの削除
DROP TABLE tasks_20240811;
