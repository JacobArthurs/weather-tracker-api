from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Forecast

router = APIRouter(
    prefix="/forecasts",
    tags=["forecasts"]
)


@router.get("/")
def read_forecasts(lat: float, lon: float, date: date, utc_hour: int = Query(ge=0, le=23), db: Session = Depends(get_db)):
    result = (
        db.query(
            func.min(Forecast.temperature).label("low"),
            func.max(Forecast.temperature).label("high"),
            Forecast.temperature_unit,
        )
        .filter(
            Forecast.lat == round(lat, 4),
            Forecast.lon == round(lon, 4),
            Forecast.forecast_date == date,
            Forecast.forecast_hour == utc_hour,
        )
        .group_by(Forecast.temperature_unit)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="No forecasts found for the given parameters")

    return {
        "low": result.low,
        "high": result.high,
        "unit": result.temperature_unit,
    }
