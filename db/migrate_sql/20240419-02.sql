-- carsの列順変更

-- テーブルのバックアップ
SELECT * INTO cars_20240419
FROM cars;

-- テーブルの削除
DROP TABLE cars;

-- テーブルの作成
CREATE TABLE cars (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying NOT NULL,
    seq integer NOT NULL,
    maker character varying NOT NULL,
    model character varying NOT NULL,
    model_year integer NOT NULL,
    license_plate character varying,
    tank_capacity integer,
    uid character varying NOT NULL,
    created_at timestamp(6) without time zone NOT NULL,
    updated_at timestamp(6) without time zone NOT NULL
);
ALTER TABLE ONLY cars ADD CONSTRAINT cars_pkey PRIMARY KEY (id);
CREATE UNIQUE INDEX index_cars_on_seq_and_uid ON cars USING btree (seq, uid);

-- データの戻し
INSERT INTO cars
SELECT
  id,
  name,
  ROW_NUMBER() OVER(ORDER BY id),
  maker,
  model,
  model_year,
  license_plate,
  tank_capacity,
  'MhpgUUWTcAMTpI1zvTcKRJlxysk1',
  created_at,
  updated_at
FROM cars_20240419;

-- バックアップテーブルの削除
DROP TABLE cars_20240419;
