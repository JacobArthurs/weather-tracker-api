from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .forecasts import Forecast

__all__ = ["Forecast"]