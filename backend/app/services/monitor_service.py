import random
from typing import TypedDict


class MonitorData(TypedDict):
    soil_moisture: int
    temperature: int
    humidity: int


def get_monitor_data() -> MonitorData:
    return {
        "soil_moisture": random.randint(20, 80),
        "temperature": random.randint(20, 40),
        "humidity": random.randint(40, 90),
    }
