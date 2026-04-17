import random

def get_monitor_data():
    return {
        "soil_moisture": random.randint(20, 80),
        "temperature": random.randint(20, 40),
        "humidity": random.randint(40, 90)
    }