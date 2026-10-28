import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from models import Base

DATABASE_URL = "postgresql://azaliavagizova@localhost:5432/moscow_bi"

def init_db():
    print("Подключаемся к базе данных...")
    engine = create_engine(DATABASE_URL)

    print("Создаем таблицы...")
    Base.metadata.create_all(engine)

    print("Готово! Все таблицы созданы.")

if __name__ == "__main__":
    init_db()
