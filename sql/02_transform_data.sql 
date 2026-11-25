-- УРОВЕНЬ ЖИЗНИ (Доходы, Бедность, Пенсии)
INSERT INTO fact_living_standard (indicator_id, year_id, value_numeric)
SELECT (SELECT indicator_id
FROM dim_indicator
WHERE code = 'INCOME_TOTAL'),
dy.year_id,
CAST(s.value_raw AS NUMERIC)
FROM stg_raw_data s
JOIN dim_year dy ON s.year = dy.year_value
WHERE s.indicator_name LIKE '%Денежные доходы%'
AND s.value_raw ~ '^[0-9.]+$'
AND s.indicator_name NOT LIKE '%на душу%';

INSERT INTO fact_living_standard (indicator_id, year_id, value_numeric)
SELECT (SELECT indicator_id
FROM dim_indicator
WHERE code = 'POVERTY'),
dy.year_id,
CAST(s.value_raw AS NUMERIC)
FROM stg_raw_data s
JOIN dim_year dy ON s.year = dy.year_value
WHERE s.indicator_name LIKE '%прожиточного минимума%'
AND s.value_raw ~ '^[0-9.]+$';

INSERT INTO fact_living_standard (indicator_id, year_id, value_numeric)
SELECT (SELECT indicator_id
FROM dim_indicator
WHERE code = 'PENSION_AVG'),
dy.year_id,
CAST(s.value_raw AS NUMERIC)
FROM stg_raw_data s
JOIN dim_year dy ON s.year = dy.year_value
WHERE s.indicator_name LIKE '%Средний размер назначенных пенсий%'
AND s.value_raw ~ '^[0-9.]+$';

-- ЗДРАВООХРАНЕНИЕ (Врачи, Медсестры, Койки)
INSERT INTO fact_healthcare (indicator_id, year_id, value_numeric)
SELECT (SELECT indicator_id
FROM dim_indicator
WHERE code = 'DOCTORS'),
dy.year_id,
CAST(s.value_raw AS NUMERIC)
FROM stg_raw_data s
JOIN dim_year dy ON s.year = dy.year_value
WHERE s.indicator_name LIKE '%Численность врачей%'
AND s.value_raw ~ '^[0-9.]+$'
AND CAST(s.value_raw AS NUMERIC) > 1000;

INSERT INTO fact_healthcare (indicator_id, year_id, value_numeric)
SELECT (SELECT indicator_id
FROM dim_indicator
WHERE code = 'NURSES'),
dy.year_id,
CAST(s.value_raw AS NUMERIC)
FROM stg_raw_data s
JOIN dim_year dy ON s.year = dy.year_value
WHERE s.indicator_name LIKE '%среднего медицинского персонала%'
AND s.value_raw ~ '^[0-9.]+$'
AND CAST(s.value_raw AS NUMERIC) > 1000;

-- ОБРАЗОВАНИЕ И СПОРТ (Садики, Спорт)
INSERT INTO fact_education_sport (indicator_id, year_id, value_numeric)
SELECT (SELECT indicator_id
FROM dim_indicator
WHERE code = 'KINDERGARTEN_KIDS'),
dy.year_id,
CAST(s.value_raw AS NUMERIC)
FROM stg_raw_data s
JOIN dim_year dy ON s.year = dy.year_value
WHERE s.indicator_name LIKE '%воспитанников%'
AND s.value_raw ~ '^[0-9.]+$';

-- ЦЕНЫ И ИНФЛЯЦИЯ (Бензин, Молоко)
INSERT INTO dim_indicator (code, name, unit, category) VALUES
('PRICE_GASOLINE', 'Средняя цена на бензин', 'руб./л', 'Цены'),
('PRICE_MILK', 'Средняя цена на молоко', 'руб./л', 'Цены'),
('CPI_TOTAL', 'Сводный индекс потребительских цен', '%', 'Цены')
ON CONFLICT (code) DO NOTHING;

-- Бензин
INSERT INTO fact_prices (indicator_id, year_id, value_numeric)
SELECT (SELECT indicator_id
FROM dim_indicator
WHERE code = 'PRICE_GASOLINE'),
dy.year_id,
CAST(s.value_raw AS NUMERIC)
FROM stg_raw_data s
JOIN dim_year dy ON s.year = dy.year_value
WHERE (s.indicator_name LIKE '%нефтепродукты%' OR s.indicator_name LIKE '%бензин%')
AND s.value_raw ~ '^[0-9.]+$';

-- Молоко
INSERT INTO fact_prices (indicator_id, year_id, value_numeric)
SELECT (SELECT indicator_id
FROM dim_indicator
WHERE code = 'PRICE_MILK'),
dy.year_id,
CAST(s.value_raw AS NUMERIC)
FROM stg_raw_data s
JOIN dim_year dy ON s.year = dy.year_value
WHERE s.indicator_name LIKE '%молоко%'
AND s.value_raw ~ '^[0-9.]+$';
