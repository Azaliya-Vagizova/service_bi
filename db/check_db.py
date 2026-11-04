from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://azaliavagizova@localhost:5432/moscow_bi"
engine = create_engine(DATABASE_URL)

def check_data():
    with engine.connect() as conn:
        count_fact = conn.execute(text("SELECT COUNT(*) FROM fact_indicator_value")).scalar()
        print(f"Всего записей в fact_indicator_value: {count_fact}")

        count_morb = conn.execute(text("SELECT COUNT(*) FROM fact_morbidity")).scalar()
        print(f"Всего записей в fact_morbidity: {count_morb}")

        if count_fact > 0:
            print("\nПервые 5 строк из fact_indicator_value:")
            result = conn.execute(text("SELECT indicator_id, year_id, value_numeric FROM fact_indicator_value LIMIT 5"))
            for row in result:
                print(f"Показатель ID: {row[0]}, Год ID: {row[1]}, Значение: {row[2]}")

        count_ind = conn.execute(text("SELECT COUNT(*) FROM dim_indicator")).scalar()
        print(f"\nВсего показателей в dim_indicator: {count_ind}")

if __name__ == "__main__":
    check_data()
