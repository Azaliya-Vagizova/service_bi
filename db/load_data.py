import sys
import os
import pandas as pd
import glob
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://azaliavagizova@localhost:5432/moscow_bi"
engine = create_engine(DATABASE_URL)

data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'raw')

def load_data():
    print("Начинаем загрузку данных...")

    with engine.connect() as conn:
        income_file = glob.glob(os.path.join(data_path, 'inc_6_*.xlsx'))[0]
        df_inc = pd.read_excel(income_file, header=None)
        years = df_inc.iloc[2, 1:].values
        incomes = df_inc.iloc[3, 1:].values

        for y, i in zip(years, incomes):
            try:
                year_num = int(float(str(y)))
                income_num = float(str(i))

                ind_id = conn.execute(text("SELECT indicator_id FROM dim_indicator WHERE code='INCOME'")).scalar()
                year_id = conn.execute(text("SELECT year_id FROM dim_year WHERE year_value=:y"), {"y": year_num}).scalar()

                if ind_id and year_id:
                    conn.execute(text("""
                        INSERT INTO fact_indicator_value (indicator_id, year_id, value_numeric)
                        VALUES (:ind, :yr, :val)
                        ON CONFLICT DO NOTHING
                    """), {"ind": ind_id, "yr": year_id, "val": income_num})
            except ValueError:
                continue
        print("Доходы загружены!")

        pov_file = glob.glob(os.path.join(data_path, 'inc_14_*.xlsx'))[0]
        df_pov = pd.read_excel(pov_file, header=None)
        years_pov = df_pov.iloc[3:, 0].values
        vals_pov = df_pov.iloc[3:, 1].values

        for y, v in zip(years_pov, vals_pov):
            try:
                year_num = int(float(str(y)))
                val_num = float(str(v))

                ind_id = conn.execute(text("SELECT indicator_id FROM dim_indicator WHERE code='POVERTY'")).scalar()
                year_id = conn.execute(text("SELECT year_id FROM dim_year WHERE year_value=:y"), {"y": year_num}).scalar()

                if ind_id and year_id:
                    conn.execute(text("""
                        INSERT INTO fact_indicator_value (indicator_id, year_id, value_numeric)
                        VALUES (:ind, :yr, :val)
                        ON CONFLICT DO NOTHING
                    """), {"ind": ind_id, "yr": year_id, "val": val_num})
            except ValueError:
                continue
        print("Бедность загружена!")

        staff_file = glob.glob(os.path.join(data_path, 'health_21_*.xlsx'))[0]
        df_staff = pd.read_excel(staff_file, header=None)
        years_staff = df_staff.iloc[8:, 0].values
        doctors = df_staff.iloc[8:, 1].values

        for y, d in zip(years_staff, doctors):
            try:
                y_str = str(y).strip()
                if y_str != 'nan':
                    year_num = int(float(y_str.split()[0]))
                    doc_num = float(str(d))

                    ind_id = conn.execute(text("SELECT indicator_id FROM dim_indicator WHERE code='MEDICAL_STAFF'")).scalar()
                    year_id = conn.execute(text("SELECT year_id FROM dim_year WHERE year_value=:y"), {"y": year_num}).scalar()

                    if ind_id and year_id:
                        conn.execute(text("""
                            INSERT INTO fact_indicator_value (indicator_id, year_id, value_numeric)
                            VALUES (:ind, :yr, :val)
                            ON CONFLICT DO NOTHING
                        """), {"ind": ind_id, "yr": year_id, "val": doc_num})
            except ValueError:
                continue
        print("Медкадры загружены!")

        conn.commit() # Сохраняем изменения в базе
    print("Все данные успешно загружены в базу!")

if __name__ == "__main__":
    load_data()
