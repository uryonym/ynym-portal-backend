-- refuelingsの列の修正

-- テーブルのバックアップ
SELECT * INTO refuelings_20240420
FROM refuelings;

-- テーブルの削除
DROP TABLE refuelings;

-- テーブルの作成
CREATE TABLE refuelings (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    refuel_datetime timestamp(6) without time zone NOT NULL,
    odometer integer NOT NULL,
    fuel_type character varying NOT NULL,
    price integer NOT NULL,
    total_cost integer NOT NULL,
    is_full boolean DEFAULT true NOT NULL,
    gas_stand character varying NOT NULL,
    uid character varying NOT NULL,
    car_id uuid NOT NULL,
    created_at timestamp(6) without time zone NOT NULL,
    updated_at timestamp(6) without time zone NOT NULL
);
ALTER TABLE ONLY refuelings ADD CONSTRAINT refuelings_pkey PRIMARY KEY (id);

-- データの戻し
INSERT INTO refuelings
SELECT
  id,
  refuel_datetime,
  odometer,
  fuel_type,
  price,
  total_cost,
  full_flag,
  gas_stand,
  'MhpgUUWTcAMTpI1zvTcKRJlxysk1',
  car_id,
  created_at,
  updated_at
FROM refuelings_20240420;

-- バックアップテーブルの削除
DROP TABLE refuelings_20240420;
