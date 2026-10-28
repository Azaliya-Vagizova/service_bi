from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
import uvicorn

app = FastAPI(title="Мониторинг качества жизни г. Москвы")
engine = create_engine("postgresql://azaliavagizova@localhost:5432/moscow_bi")

@app.get("/indicator/{code}/{year}")
def get_indicator(code: str, year: int):
    """Получение значения показателя за конкретный год"""
    with engine.connect() as conn:
        query = text("""
            SELECT di.name, dy.year_value, fiv.value_numeric, di.unit
            FROM fact_indicator_value fiv
            JOIN dim_indicator di ON fiv.indicator_id = di.indicator_id
            JOIN dim_year dy ON fiv.year_id = dy.year_id
            WHERE di.code = :code AND dy.year_value = :year
        """)
        result = conn.execute(query, {"code": code.upper(), "year": year}).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Данные не найдены")

        return {
            "indicator": result[0],
            "year": result[1],
            "value": float(result[2]),
            "unit": result[3]
        }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
