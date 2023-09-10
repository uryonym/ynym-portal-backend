# tasksの列追加

# テーブルのバックアップ
select * into tasks_20230906
from tasks;

# テーブルの削除
drop table tasks;

# テーブルの作成
create table tasks (
  id uuid default gen_random_uuid() not null,
  title character varying not null,
  description character varying,
  dead_line date,
  is_complete boolean default false not null,
  uid character varying not null,
  task_list_id uuid not null,
  created_at timestamp(6) without time zone not null,
  updated_at timestamp(6) without time zone not null
);

# データの戻し
insert into tasks
select
  id,
  title,
  description,
  dead_line,
  is_complete,
  'uTnu3ZWTGRUV4gglrxMsYJupoRI3',
  '0427e51f-ab6b-47c4-a41d-25d489156d7e',
  created_at,
  updated_at
from tasks_20230906;

# バックアップテーブルの削除
drop table tasks_20230906;
