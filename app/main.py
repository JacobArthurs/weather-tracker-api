import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

from app.routers import forecasts
from app import scheduler


@asynccontextmanager
async def lifespan(_app: FastAPI):
    scheduler.start()
    yield
    scheduler.stop()


app = FastAPI(
    title="Weather Tracker API",
    description="A simple API to track weather forecasts.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Welcome to Weather Tracker API!"}
