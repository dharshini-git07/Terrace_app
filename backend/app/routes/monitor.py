from fastapi import APIRouter
from app.services.monitor_service import get_monitor_data
from app.agents.plant_health_agent import check_plant_health
from app.agents.water_management_agent import water_management

router = APIRouter(prefix="/monitor", tags=["Monitor"])

# Common function to avoid repeating code
def fetch_data():
    return get_monitor_data()


# 📊 Get Raw Sensor Data
@router.get("/data")
def get_data():
    return fetch_data()
# 🌿 Plant Health
@router.get("/plant-health")
def plant_health():
    data = fetch_data()
    return check_plant_health(data)


# 💧 Water Management
@router.get("/water-management")
def water_manage():
    data = fetch_data()
    return water_management(data)