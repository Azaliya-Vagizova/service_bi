from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

# СЛОЙ 1: STAGING (СЫРЫЕ ДАННЫЕ)
class StgRawData(Base):
    __tablename__ = 'stg_raw_data'
    raw_id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String(255))
    indicator_name = Column(String(255))
    year = Column(Integer, nullable=True)
    value_raw = Column(String(100))
    loaded_at = Column(DateTime, default=datetime.utcnow)

# СЛОЙ 2: СПРАВОЧНИКИ (DIMENSIONS)
class DimIndicator(Base):
    __tablename__ = 'dim_indicator'
    indicator_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    unit = Column(String(50))
    category = Column(String(100))

class DimYear(Base):
    __tablename__ = 'dim_year'
    year_id = Column(Integer, primary_key=True, autoincrement=True)
    year_value = Column(Integer, unique=True, nullable=False)

class DimMonth(Base):
    __tablename__ = 'dim_month'
    month_id = Column(Integer, primary_key=True, autoincrement=True)
    month_name = Column(String(20), nullable=False)

class DimDiseaseClass(Base):
    __tablename__ = 'dim_disease_class'
    disease_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

class DimCpiCategory(Base):
    __tablename__ = 'dim_cpi_category'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

# СЛОЙ 3: ВИТРИНЫ ДАННЫХ (FACTS)
class FactLivingStandard(Base):
    __tablename__ = 'fact_living_standard'
    fact_id = Column(Integer, primary_key=True, autoincrement=True)
    indicator_id = Column(Integer, ForeignKey('dim_indicator.indicator_id'))
    year_id = Column(Integer, ForeignKey('dim_year.year_id'))
    value_numeric = Column(Numeric)

class FactHealthcare(Base):
    __tablename__ = 'fact_healthcare'
    fact_id = Column(Integer, primary_key=True, autoincrement=True)
    indicator_id = Column(Integer, ForeignKey('dim_indicator.indicator_id'))
    year_id = Column(Integer, ForeignKey('dim_year.year_id'))
    disease_id = Column(Integer, ForeignKey('dim_disease_class.disease_id'), nullable=True)
    value_numeric = Column(Numeric)

class FactPrices(Base):
    __tablename__ = 'fact_prices'
    fact_id = Column(Integer, primary_key=True, autoincrement=True)
    indicator_id = Column(Integer, ForeignKey('dim_indicator.indicator_id'))
    year_id = Column(Integer, ForeignKey('dim_year.year_id'))
    month_id = Column(Integer, ForeignKey('dim_month.month_id'), nullable=True)
    category_id = Column(Integer, ForeignKey('dim_cpi_category.category_id'), nullable=True)
    value_numeric = Column(Numeric)

class FactEducationSport(Base):
    __tablename__ = 'fact_education_sport'
    fact_id = Column(Integer, primary_key=True, autoincrement=True)
    indicator_id = Column(Integer, ForeignKey('dim_indicator.indicator_id'))
    year_id = Column(Integer, ForeignKey('dim_year.year_id'))
    value_numeric = Column(Numeric)
