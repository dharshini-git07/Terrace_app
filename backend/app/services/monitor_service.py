import json
import os
import time
from urllib.error import URLError
from urllib.request import urlopen
from typing import TypedDict


class MonitorData(TypedDict):
    soil_moisture: int
    temperature: int
    humidity: int


FIREBASE_DATABASE_URL = os.getenv(
    "HARDWARE_FIREBASE_DATABASE_URL",
    "https://satf-de59f-default-rtdb.asia-southeast1.firebasedatabase.app",
).rstrip("/")
FIREBASE_DATABASE_PATHS = (
    "hardware",
    "sensorData",
    "sensors",
    "monitor",
    "monitoring",
    "data",
    "",
)
FALLBACK_MONITOR_DATA: MonitorData = {
    "soil_moisture": 65,
    "temperature": 28,
    "humidity": 70,
}
_cached_monitor_data: MonitorData | None = None
_last_fetch_time = 0.0
CACHE_SECONDS = 2


def _to_number(value: object) -> float | None:
    if value is None or value == "":
        return None

    if isinstance(value, str):
        value = (
            value.replace("%", "")
            .replace("°C", "")
            .replace("Â°C", "")
            .strip()
        )

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _find_reading(data: object, keys: set[str]) -> float | None:
    if not isinstance(data, dict):
        return None

    queue: list[object] = [data]

    while queue:
        current = queue.pop(0)
        if not isinstance(current, dict):
            continue

        for key, value in current.items():
            normalized_key = str(key).lower().replace(" ", "").replace("_", "").replace("-", "")
            if normalized_key in keys:
                number_value = _to_number(value)
                if number_value is not None:
                    return number_value

            if isinstance(value, dict):
                queue.append(value)

    return None


def _normalize_monitor_data(raw_data: object) -> MonitorData | None:
    soil_moisture = _find_reading(
        raw_data,
        {
            "soilmoisture",
            "soilmoisturepercent",
            "moisture",
            "moisturepercent",
            "soil",
            "soilwater",
            "soilwaterlevel",
        },
    )
    temperature = _find_reading(
        raw_data,
        {
            "temperature",
            "temp",
            "fieldtemperature",
            "temperaturec",
            "temperaturecelsius",
            "airtemperature",
            "airtemp",
        },
    )
    humidity = _find_reading(
        raw_data,
        {
            "humidity",
            "airhumidity",
            "humiditypercent",
            "hum",
        },
    )

    if soil_moisture is None and temperature is None and humidity is None:
        return None

    return {
        "soil_moisture": round(soil_moisture if soil_moisture is not None else FALLBACK_MONITOR_DATA["soil_moisture"]),
        "temperature": round(temperature if temperature is not None else FALLBACK_MONITOR_DATA["temperature"]),
        "humidity": round(humidity if humidity is not None else FALLBACK_MONITOR_DATA["humidity"]),
    }


def _read_firebase_path(path: str) -> object:
    firebase_path = f"/{path}" if path else ""
    url = f"{FIREBASE_DATABASE_URL}{firebase_path}.json"

    with urlopen(url, timeout=4) as response:
        return json.loads(response.read().decode("utf-8"))


def _get_firebase_monitor_data() -> MonitorData | None:
    for path in FIREBASE_DATABASE_PATHS:
        try:
            monitor_data = _normalize_monitor_data(_read_firebase_path(path))
        except (OSError, URLError, TimeoutError, json.JSONDecodeError):
            continue

        if monitor_data:
            return monitor_data

    return None


def get_monitor_data() -> MonitorData:
    global _cached_monitor_data, _last_fetch_time

    now = time.monotonic()
    if _cached_monitor_data and now - _last_fetch_time < CACHE_SECONDS:
        return _cached_monitor_data

    monitor_data = _get_firebase_monitor_data() or FALLBACK_MONITOR_DATA
    _cached_monitor_data = monitor_data
    _last_fetch_time = now
    return monitor_data
