-- 1. View для уровня жизни
CREATE OR REPLACE VIEW v_living_standard AS
SELECT di.category AS "Категория",
di.name AS "Показатель",
dy.year_value AS "Год",
f.value_numeric AS "Значение",
di.unit AS "Ед_изм"
FROM fact_living_standard f
JOIN dim_indicator di ON f.indicator_id = di.indicator_id
JOIN dim_year dy ON f.year_id = dy.year_id;

-- 2. View для здравоохранения
CREATE OR REPLACE VIEW v_healthcare AS
SELECT di.category AS "Категория",
di.name AS "Показатель",
dy.year_value AS "Год",
dc.name AS "Болезнь",
f.value_numeric AS "Значение"
FROM fact_healthcare f
JOIN dim_indicator di ON f.indicator_id = di.indicator_id
JOIN dim_year dy ON f.year_id = dy.year_id
LEFT JOIN dim_disease_class dc ON f.disease_id = dc.disease_id;

-- 3. View для цен
CREATE OR REPLACE VIEW v_prices AS
SELECT di.category AS "Категория",
di.name AS "Показатель",
dy.year_value AS "Год",
f.value_numeric AS "Значение"
FROM fact_prices f
JOIN dim_indicator di ON f.indicator_id = di.indicator_id
JOIN dim_year dy ON f.year_id = dy.year_id;

-- 4. View для образования
CREATE OR REPLACE VIEW v_education AS
SELECT di.category AS "Категория",
di.name AS "Показатель",
dy.year_value AS "Год",
f.value_numeric AS "Значение"
FROM fact_education_sport f
JOIN dim_indicator di ON f.indicator_id = di.indicator_id
JOIN dim_year dy ON f.year_id = dy.year_id;
