from fastapi import FastAPI

app = FastAPI(
    title="Weather Tracker API",
    description="A simple API to track weather forecasts.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Welcome to Weather Tracker API!"}
