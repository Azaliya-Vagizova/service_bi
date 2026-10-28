import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

print("Подключаемся к серверу PostgreSQL...")
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="azaliavagizova",
        host="localhost",
        port="5432"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'moscow_bi'")
    exists = cursor.fetchone()

    if not exists:
        print("Создаем базу данных moscow_bi...")
        cursor.execute("CREATE DATABASE moscow_bi")
        print("База данных успешно создана!")
    else:
        print("База данных moscow_bi уже существует.")

    cursor.close()
    conn.close()
except Exception as e:
    print(f"Ошибка: {e}")
