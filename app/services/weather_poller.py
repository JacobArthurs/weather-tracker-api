import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

import httpx

from app.db import SessionLocal
from app.models import Forecast

logger = logging.getLogger(__name__)

_HEADERS = {"User-Agent": "weather-tracker-api"}


def _load_location() -> tuple[float, float]:
    with Path("config.json").open() as f:
        loc = json.load(f)["location"]
    return round(float(loc["lat"]), 4), round(float(loc["lon"]), 4)


def poll_weather() -> None:
    try:
        lat, lon = _load_location()
    except Exception:
        logger.exception("Failed to load location from config.json")
        return

    hourly_url = _get_hourly_forecast_url(lat, lon)
    if not hourly_url:
        return

    try:
        r = httpx.get(hourly_url, headers=_HEADERS, timeout=30)
        r.raise_for_status()
    except httpx.HTTPError:
        logger.exception("Failed to fetch hourly forecast for (%s, %s)", lat, lon)
        return

    cutoff = datetime.now(timezone.utc) + timedelta(hours=72)
    periods = [
        (dt, p)
        for p in r.json()["properties"]["periods"]
        if (dt := datetime.fromisoformat(p["startTime"])) <= cutoff
    ]

    db = SessionLocal()
    try:
        db.add_all(
            Forecast(
                lat=lat,
                lon=lon,
                forecast_date=(dt_utc := dt.astimezone(timezone.utc)).date(),
                forecast_hour=dt_utc.hour,
                temperature=period["temperature"],
                temperature_unit=period["temperatureUnit"],
            )
            for dt, period in periods
        )
        db.commit()
        logger.info("Inserted %d forecast rows for (%s, %s)", len(periods), lat, lon)
    except Exception:
        db.rollback()
        logger.exception("Failed to insert forecasts for (%s, %s)", lat, lon)
    finally:
        db.close()


def _get_hourly_forecast_url(lat: float, lon: float) -> str | None:
    url = f"https://api.weather.gov/points/{lat},{lon}"
    try:
        r = httpx.get(url, headers=_HEADERS, timeout=30)
        r.raise_for_status()
        return r.json()["properties"]["forecastHourly"]
    except (httpx.HTTPError, KeyError):
        logger.exception("Failed to get hourly forecast URL for (%s, %s)", lat, lon)
        return None
