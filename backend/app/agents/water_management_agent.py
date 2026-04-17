def water_management(data):
    action = "No watering needed"

    if data["soil_moisture"] < 30:
        action = "Start irrigation immediately"

    elif data["soil_moisture"] < 50:
        action = "Water plants moderately"

    elif data["temperature"] > 35:
        action = "Increase watering due to heat"

    return {
        "water_action": action
    }