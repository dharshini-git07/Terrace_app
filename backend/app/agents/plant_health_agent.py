def check_plant_health(data):
    health_status = "Healthy"

    if data["temperature"] > 38:
        health_status = "Heat Stress"

    elif data["humidity"] < 40:
        health_status = "Low Humidity Stress"

    elif data["soil_moisture"] < 30:
        health_status = "Water Stress"

    return {
        "plant_health": health_status
    }