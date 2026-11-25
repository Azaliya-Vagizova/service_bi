SELECT 'Уровень жизни' as "Витрина", COUNT(*) as "Строк"
FROM fact_living_standard

UNION ALL

SELECT 'Здравоохранение', COUNT(*)
FROM fact_healthcare

UNION ALL

SELECT 'Образование и спорт', COUNT(*)
FROM fact_education_sport

UNION ALL

SELECT
'Цены', COUNT(*)
FROM fact_prices;
