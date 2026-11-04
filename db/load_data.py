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

def load_data():
    print("Начинаем загрузку данных...")

    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE fact_indicator_value, fact_morbidity CASCADE"))

        # ДОХОДЫ (inc_6)
        try:
            df = pd.read_excel(glob.glob(os.path.join(data_path, 'inc_6_*.xlsx'))[0], header=None)
            ind_id = get_ind_id(conn, 'INCOME_TOTAL')
            count = 0
            for y, val in zip(range(2014, 2025), df.iloc[3, 1:12].values):
                year_id = get_year_id(conn, y)
                if year_id and ind_id:
                    try:
                        conn.execute(text("INSERT INTO fact_indicator_value (indicator_id, year_id, value_numeric) VALUES (:i, :y, :v)"), {"i": ind_id, "y": year_id, "v": float(str(val))})
                        count += 1
                    except: pass
            print(f"Доходы загружены: {count} строк")
        except Exception as e: print(f"Ошибка доходы: {e}")

        # БЕДНОСТЬ (inc_14)
        try:
            df = pd.read_excel(glob.glob(os.path.join(data_path, 'inc_14_*.xlsx'))[0], header=None)
            ind_id = get_ind_id(conn, 'POVERTY')
            count = 0
            for y, v in zip(df.iloc[3:, 0].values, df.iloc[3:, 1].values):
                try:
                    year_num = int(float(str(y).split()[0]))
                    year_id = get_year_id(conn, year_num)
                    if year_id and ind_id:
                        conn.execute(text("INSERT INTO fact_indicator_value (indicator_id, year_id, value_numeric) VALUES (:i, :y, :v)"), {"i": ind_id, "y": year_id, "v": float(str(v))})
                        count += 1
                except: pass
            print(f"Бедность загружена: {count} строк")
        except Exception as e: print(f"Ошибка бедность: {e}")

        # ПЕНСИИ (inc_8)
        try:
            df = pd.read_excel(glob.glob(os.path.join(data_path, 'inc_8_*.xlsx'))[0], header=None)
            ind_id = get_ind_id(conn, 'PENSION_AVG')
            count = 0
            years_raw = df.iloc[4, 1:].values
            values_raw = df.iloc[6, 1:].values

            for y, v in zip(years_raw, values_raw):
                try:
                    y_str = str(y).strip()
                    if y_str == 'nan' or y_str == '': continue
                    year_num = int(float(y_str.split()[0]))

                    if year_num == 2017 and pd.isna(v): continue

                    year_id = get_year_id(conn, year_num)
                    if year_id and ind_id:
                        conn.execute(text("INSERT INTO fact_indicator_value (indicator_id, year_id, value_numeric) VALUES (:i, :y, :v)"), {"i": ind_id, "y": year_id, "v": float(str(v))})
                        count += 1
                except: pass
            print(f"Пенсии загружены: {count} строк")
        except Exception as e: print(f"Ошибка пенсии: {e}")

        # МЕДКАДРЫ (health_6)
        try:
            df = pd.read_excel(glob.glob(os.path.join(data_path, 'health_6_*.xlsx'))[0], header=None)
            years = list(range(2020, 2025))
            doc_id = get_ind_id(conn, 'DOCTORS')
            nur_id = get_ind_id(conn, 'NURSES')
            count = 0
            for y, doc, nur in zip(years, df.iloc[4:9, 1].values, df.iloc[4:9, 3].values):
                year_id = get_year_id(conn, y)
                if year_id:
                    try:
                        conn.execute(text("INSERT INTO fact_indicator_value (indicator_id, year_id, value_numeric) VALUES (:i, :y, :v)"), {"i": doc_id, "y": year_id, "v": float(str(doc))})
                        conn.execute(text("INSERT INTO fact_indicator_value (indicator_id, year_id, value_numeric) VALUES (:i, :y, :v)"), {"i": nur_id, "y": year_id, "v": float(str(nur))})
                        count += 2
                    except: pass
            print(f"Медкадры загружены: {count} строк")
        except Exception as e: print(f"Ошибка медкадры: {e}")

        # БОЛЬНИЧНЫЕ КОЙКИ (health_8)
        try:
            df = pd.read_excel(glob.glob(os.path.join(data_path, 'health_8_*.xlsx'))[0], header=None)
            ind_id = get_ind_id(conn, 'HOSPITAL_BEDS')
            years = list(range(2020, 2025))
            count = 0
            for i, row in df.iterrows():
                if "Всего" in str(row[0]):
                    for y, val in zip(years, row[1:6].values):
                        year_id = get_year_id(conn, y)
                        if year_id and ind_id:
                            try:
                                conn.execute(text("INSERT INTO fact_indicator_value (indicator_id, year_id, value_numeric) VALUES (:i, :y, :v)"), {"i": ind_id, "y": year_id, "v": float(str(val))})
                                count += 1
                            except: pass
                    break
            print(f"Больничные койки загружены: {count} строк")
        except Exception as e: print(f"Ошибка койки: {e}")

        # ЗАБОЛЕВАЕМОСТЬ (health_3)
        try:
            df = pd.read_excel(glob.glob(os.path.join(data_path, 'health_3_*.xlsx'))[0], header=None)
            count = 0

            disease_ids = [row[0] for row in conn.execute(text("SELECT disease_id FROM dim_disease_class ORDER BY disease_id")).fetchall()]

            cases = df.iloc[7:22, 5].values
            year_id = get_year_id(conn, 2024)

            for dis_id, val in zip(disease_ids, cases):
                try:
                    val_float = float(str(val))
                    if year_id and not pd.isna(val_float):
                        conn.execute(text("INSERT INTO fact_morbidity (disease_id, year_id, cases_count) VALUES (:d, :y, :v)"), {"d": dis_id, "y": year_id, "v": val_float})
                        count += 1
                except Exception as e:
                    print(f"Ошибка при вставке ID {dis_id}: {e}")
                    conn.rollback()
                    break

            print(f"Заболеваемость загружена: {count} строк")
        except Exception as e: print(f"Ошибка заболеваемость: {e}")

        conn.commit()
    print("Все данные успешно загружены!")

if __name__ == "__main__":
    load_data()
