-- notesの列追加

-- テーブルのバックアップ
select * into notes_20240106
from notes;

-- テーブルの削除
drop table notes;

-- テーブルの作成
create table notes (
  id uuid default gen_random_uuid() not null,
  title character varying not null,
  uid character varying not null,
  seq integer NOT NULL,
  created_at timestamp(6) without time zone not null,
  updated_at timestamp(6) without time zone not null
);

-- データの戻し
insert into notes
select
  id,
  title,
  'uTnu3ZWTGRUV4gglrxMsYJupoRI3',
  0,
  created_at,
  updated_at
from notes_20240106;

-- バックアップテーブルの削除
drop table notes_20240106;
