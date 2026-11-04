import sys
import os
import pandas as pd
import glob
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://azaliavagizova@localhost:5432/moscow_bi"
engine = create_engine(DATABASE_URL)
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'raw')

def get_ind_id(conn, code):
    return conn.execute(text("SELECT indicator_id FROM dim_indicator WHERE code = :c"), {"c": code}).scalar()

def get_year_id(conn, year):
    return conn.execute(text("SELECT year_id FROM dim_year WHERE year_value = :y"), {"y": year}).scalar()

def insert_fact(conn, table, ind_code, year, val, disease_id=None):
    ind_id = get_ind_id(conn, ind_code)
    year_id = get_year_id(conn, year)
    if ind_id and year_id:
        try:
            if table == 'fact_healthcare' and disease_id:
                conn.execute(text(f"INSERT INTO {table} (indicator_id, year_id, disease_id, value_numeric) VALUES (:i, :y, :d, :v)"), {"i": ind_id, "y": year_id, "d": disease_id, "v": float(str(val))})
            else:
                conn.execute(text(f"INSERT INTO {table} (indicator_id, year_id, value_numeric) VALUES (:i, :y, :v)"), {"i": ind_id, "y": year_id, "v": float(str(val))})
        except: pass

def load_all_facts():
    print("ЗАГРУЗКА ДАННЫХ В ВИТРИНЫ")

    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE fact_living_standard, fact_healthcare, fact_prices, fact_education_sport CASCADE"))
        conn.commit()

        # УРОВЕНЬ ЖИЗНИ
        try:
            # Доходы (inc_6)
            df = pd.read_excel(glob.glob(os.path.join(data_path, 'inc_6_*.xlsx'))[0], header=None)
            for y, val in zip(range(2014, 2025), df.iloc[3, 1:12].values):
                insert_fact(conn, 'fact_living_standard', 'INCOME_TOTAL', y, val)

            # Бедность (inc_14)
            df = pd.read_excel(glob.glob(os.path.join(data_path, 'inc_14_*.xlsx'))[0], header=None)
            for y, val in zip(df.iloc[3:, 0].values, df.iloc[3:, 1].values):
                try: insert_fact(conn, 'fact_living_standard', 'POVERTY', int(float(str(y).split()[0])), val)
                except: pass

            # Пенсии (inc_8)
            df = pd.read_excel(glob.glob(os.path.join(data_path, 'inc_8_*.xlsx'))[0], header=None)
            for y, val in zip(df.iloc[4, 1:].values, df.iloc[6, 1:].values):
                try: insert_fact(conn, 'fact_living_standard', 'PENSION_AVG', int(float(str(y).split()[0])), val)
                except: pass
            print("Уровень жизни загружен!")
        except Exception as e: print(f"Ошибка уровня жизни: {e}")

        # ЗДРАВООХРАНЕНИЕ
        try:
            # Медкадры (health_6)
            df = pd.read_excel(glob.glob(os.path.join(data_path, 'health_6_*.xlsx'))[0], header=None)
            for y, doc, nur in zip(range(2020, 2025), df.iloc[4:9, 1].values, df.iloc[4:9, 3].values):
                insert_fact(conn, 'fact_healthcare', 'DOCTORS', y, doc)
                insert_fact(conn, 'fact_healthcare', 'NURSES', y, nur)

            # Койки (health_8)
            df = pd.read_excel(glob.glob(os.path.join(data_path, 'health_8_*.xlsx'))[0], header=None)
            for i, row in df.iterrows():
                if "Всего" in str(row[0]):
                    for y, val in zip(range(2020, 2025), row[1:6].values):
                        insert_fact(conn, 'fact_healthcare', 'HOSPITAL_BEDS', y, val)
                    break

            # Заболеваемость (health_3)
            df = pd.read_excel(glob.glob(os.path.join(data_path, 'health_3_*.xlsx'))[0], header=None)
            dis_ids = [r[0] for r in conn.execute(text("SELECT disease_id FROM dim_disease_class ORDER BY disease_id")).fetchall()]
            for dis_id, val in zip(dis_ids, df.iloc[7:23, 5].values):
                insert_fact(conn, 'fact_healthcare', 'MORBIDITY', 2024, val, disease_id=dis_id)
            print("Здравоохранение загружено!")
        except Exception as e: print(f"Ошибка здравоохранения: {e}")

        # ОБРАЗОВАНИЕ И СПОРТ
        try:
            # Садики (health_9)
            df = pd.read_excel(glob.glob(os.path.join(data_path, 'health_9_*.xlsx'))[0], header=None)
            for y, val in zip([2020, 2021, 2022, 2023, 2024, 2025], df.iloc[4, 1:7].values):
                insert_fact(conn, 'fact_education_sport', 'KINDERGARTEN_KIDS', y, val)

            # Спорт (health_15)
            df = pd.read_excel(glob.glob(os.path.join(data_path, 'health_15_*.xlsx'))[0], header=None)
            for y, val in zip([2020, 2021, 2022], df.iloc[4:7, 1].values):
                insert_fact(conn, 'fact_education_sport', 'SPORT_FACILITIES', y, val)
            print("Образование и спорт загружены!")
        except Exception as e: print(f"Ошибка образования: {e}")

        # ЦЕНЫ
        try:
            # Бензин (4_Средние...)
            f_gas = glob.glob(os.path.join(data_path, '4_Средние*.xlsx'))[0]
            xls_gas = pd.ExcelFile(f_gas)
            for year in range(2020, 2025):
                if str(year) in xls_gas.sheet_names:
                    df = pd.read_excel(xls_gas, sheet_name=str(year), header=None)
                    for i, row in df.iterrows():
                        if "АИ-92" in str(row[1]):
                            insert_fact(conn, 'fact_prices', 'PRICE_GASOLINE', year, row[2])
                            break

            # Молоко (3_Средние...)
            f_milk = glob.glob(os.path.join(data_path, '3_Средние*.xlsx'))[0]
            xls_milk = pd.ExcelFile(f_milk)
            for year in range(2020, 2025):
                if str(year) in xls_milk.sheet_names:
                    df = pd.read_excel(xls_milk, sheet_name=str(year), header=None)
                    insert_fact(conn, 'fact_prices', 'PRICE_MILK', year, df.iloc[15, 1])
            print("Цены загружены!")
        except Exception as e: print(f"Ошибка цен: {e}")

        conn.commit()

        print("\nИТОГОВАЯ ПРОВЕРКА")
        for table, name in [('fact_living_standard', 'Уровень жизни'), ('fact_healthcare', 'Здравоохранение'), ('fact_education_sport', 'Образование'), ('fact_prices', 'Цены')]:
            cnt = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"{name}: {cnt} строк")

if __name__ == "__main__":
    load_all_facts()
