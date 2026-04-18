import os
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app.services.weather_poller import poll_weather

_scheduler = BackgroundScheduler()


def start() -> None:
    interval_minutes = int(os.getenv("POLL_INTERVAL_MINUTES", "60"))
    _scheduler.add_job(
        poll_weather,
        "interval",
        minutes=interval_minutes,
        id="weather_poll",
        next_run_time=datetime.now(),
    )
    _scheduler.start()


def stop() -> None:
    _scheduler.shutdown(wait=True)
