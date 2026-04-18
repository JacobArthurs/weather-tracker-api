# Weather Tracker API

A FastAPI service that polls weather forecasts on a schedule and exposes them via a REST API. Uses the [weather.gov API](https://www.weather.gov/documentation/services-web-api) and stores data in PostgreSQL.

## Prerequisites

- Docker & Docker Compose

## Configuration

1. Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

`.env.example` documents all available variables:

| Variable | Default | Description |
| --- | --- | --- |
| `POSTGRES_USER` | `postgres` | Database user |
| `POSTGRES_PASSWORD` | `password` | Database password |
| `POSTGRES_DB` | `weather_tracker_db` | Database name |
| `POLL_INTERVAL_MINUTES` | `60` | How often to fetch forecasts |

2. Copy the example config and set your target location:

```bash
cp config.json.example config.json
```

```json
{
    "location": {
        "lat": "42.3390",
        "lon": "-83.0486"
    }
}
```

## Build & Run

```bash
docker compose up -d --build
```

The API will be available at `http://localhost:8000`.

## API

Interactive docs: `http://localhost:8000/docs`

### `GET /forecasts/`

Returns the high/low temperature for a given location, date, and UTC hour.

| Parameter | Type | Description |
| --- | --- | --- |
| `lat` | float | Latitude |
| `lon` | float | Longitude |
| `date` | date | Date (`YYYY-MM-DD`) |
| `utc_hour` | int (0–23) | UTC hour |

**Example:**

```bash
curl "http://localhost:8000/forecasts/?lat=42.339&lon=-83.0486&date=2026-04-18&utc_hour=12"
```

**Response:**

```json
{
    "low": 31,
    "high": 45,
    "unit": "F"
}
```

## Assumptions

- **US locations only.** The weather.gov API only covers locations within the United States.
- **Single tracked location.** Only one lat/lon pair is read from `config.json` at a time.
- **Coordinates rounded to 4 decimal places.** Queries against stored forecasts must match to 4 decimal places (e.g. `42.3390`, not `42.34`).
- **Forecasts stored up to 72 hours ahead.** Each poll inserts hourly periods for the next 72 hours; older data is not automatically purged.
- **UTC hours.** All `forecast_hour` values and the `utc_hour` query parameter are in UTC.
- **Temperatures stored as-is from weather.gov API.** No unit conversion is performed.
