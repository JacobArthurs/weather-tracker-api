from sqlalchemy import Column, Date, Float, Integer, String, DateTime, func
from . import Base

class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    forecast_date = Column(Date, nullable=False)
    forecast_hour = Column(Integer, nullable=False)
    temperature = Column(Integer, nullable=False)
    temperature_unit = Column(String(1), nullable=False)
    retrieved_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)