from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

# Справочник показателей (Доходы, Бедность, ИПЦ и т.д.)
class DimIndicator(Base):
    __tablename__ = 'dim_indicator'

    indicator_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    unit = Column(String(50))

# Справочник лет
class DimYear(Base):
    __tablename__ = 'dim_year'

    year_id = Column(Integer, primary_key=True, autoincrement=True)
    year_value = Column(Integer, unique=True, nullable=False)

# Таблица фактов (основные цифры)
class FactIndicatorValue(Base):
    __tablename__ = 'fact_indicator_value'

    value_id = Column(Integer, primary_key=True, autoincrement=True)
    indicator_id = Column(Integer, ForeignKey('dim_indicator.indicator_id'))
    year_id = Column(Integer, ForeignKey('dim_year.year_id'))
    value_numeric = Column(Numeric)
    loaded_at = Column(DateTime, default=datetime.utcnow)

# Справочник болезней (для круговой диаграммы)
class DimDiseaseClass(Base):
    __tablename__ = 'dim_disease_class'

    disease_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

# Таблица фактов по заболеваемости
class FactMorbidity(Base):
    __tablename__ = 'fact_morbidity'

    morbidity_id = Column(Integer, primary_key=True, autoincrement=True)
    disease_id = Column(Integer, ForeignKey('dim_disease_class.disease_id'))
    year_id = Column(Integer, ForeignKey('dim_year.year_id'))
    cases_count = Column(Numeric)
    loaded_at = Column(DateTime, default=datetime.utcnow)
