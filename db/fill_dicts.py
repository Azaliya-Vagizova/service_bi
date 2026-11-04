from sqlalchemy import create_engine, text
import sys

DATABASE_URL = "postgresql://azaliavagizova@localhost:5432/moscow_bi"
engine = create_engine(DATABASE_URL)

def fill_dictionaries():
    print("Начинаем заполнение справочников...")

    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE fact_cpi, fact_monthly_indicator, fact_morbidity, fact_indicator_value, dim_cpi_category, dim_disease_class, dim_indicator, dim_year CASCADE"))
        print("Старые данные очищены.")

        indicators = [
            ('INCOME_TOTAL', 'Денежные доходы населения', 'тыс. руб.', 'Уровень жизни'),
            ('INCOME_PER_CAPITA', 'Среднедушевые денежные доходы', 'руб.', 'Уровень жизни'),
            ('POVERTY', 'Доля населения с доходами ниже прожиточного минимума', '%', 'Уровень жизни'),
            ('PENSION_AVG', 'Средний размер пенсии', 'руб.', 'Уровень жизни'),
            ('CONSUMER_EXP', 'Потребительские расходы', 'тыс. руб.', 'Уровень жизни'),
            ('CHILD_BENEFIT', 'Размер ежемесячного пособия на ребенка', 'руб.', 'Уровень жизни'),
            ('CPI_TOTAL', 'Сводный индекс потребительских цен', '%', 'Цены и инфляция'),
            ('PRICE_MILK', 'Средняя цена на молоко', 'руб./л', 'Цены и инфляция'),
            ('PRICE_GASOLINE', 'Средняя цена на бензин', 'руб./л', 'Цены и инфляция'),
            ('PRICE_HOUSING_PRIMARY', 'Индекс цен на первичное жилье', '%', 'Цены и инфляция'),
            ('PRICE_HOUSING_SECONDARY', 'Индекс цен на вторичное жилье', '%', 'Цены и инфляция'),
            ('PPI_INDUSTRIAL', 'Индексы цен производителей', '%', 'Цены и инфляция'),
            ('DOCTORS', 'Численность врачей', 'чел.', 'Здравоохранение'),
            ('NURSES', 'Численность среднего медперсонала', 'чел.', 'Здравоохранение'),
            ('HOSPITAL_BEDS', 'Число больничных коек', 'шт.', 'Здравоохранение'),
            ('MED_ORGS', 'Число медицинских организаций', 'шт.', 'Здравоохранение'),
            ('KINDERGARTEN_KIDS', 'Воспитанники детских садов', 'чел.', 'Образование и досуг'),
            ('KINDERGARTEN_PLACES', 'Число мест в детских садах', 'шт.', 'Образование и досуг'),
            ('SPORT_FACILITIES', 'Количество спортивных сооружений', 'шт.', 'Образование и досуг'),
            ('SPORT_PARTICIPANTS', 'Занимающиеся в спортивных секциях', 'чел.', 'Образование и досуг')
        ]
        for code, name, unit, category in indicators:
            conn.execute(text("INSERT INTO dim_indicator (code, name, unit, category) VALUES (:c, :n, :u, :cat)"),
                         {"c": code, "n": name, "u": unit, "cat": category})
        print(f"Добавлено показателей: {len(indicators)}")

        for year in range(2011, 2025):
            conn.execute(text("INSERT INTO dim_year (year_value) VALUES (:y)"), {"y": year})
        print("Года добавлены (2011-2024)")

        cpi_cats = ['Продовольственные товары', 'Непродовольственные товары', 'Услуги']
        for cat in cpi_cats:
            conn.execute(text("INSERT INTO dim_cpi_category (name) VALUES (:n)"), {"n": cat})
        print("Категории ИПЦ добавлены")

        diseases = [
            'Болезни органов дыхания',
            'Травмы, отравления и некоторые другие последствия воздействия внешних причин',
            'Болезни кожи и подкожной клетчатки',
            'Болезни мочеполовой системы',
            'Болезни глаза и его придаточного аппарата',
            'Болезни уха и сосцевидного отростка',
            'Болезни системы кровообращения',
            'Болезни органов пищеварения',
            'Болезни костно-мышечной системы и соединительной ткани',
            'Новообразования',
            'Некоторые инфекционные и паразитарные болезни',
            'Болезни крови, кроветворных органов и отдельные нарушения, вовлекающие иммунный механизм',
            'Болезни эндокринной системы, расстройства питания, нарушения обмена веществ',
            'Болезни нервной системы',
            'Врожденные аномалии (пороки развития), деформации и хромосомные нарушения',
            'Прочие болезни'
        ]
        for dis in diseases:
            conn.execute(text("INSERT INTO dim_disease_class (name) VALUES (:n)"), {"n": dis})
        print("Классы болезней добавлены")

        conn.commit()
    print("Все справочники успешно заполнены!")

if __name__ == "__main__":
    fill_dictionaries()
