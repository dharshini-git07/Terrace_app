from fastapi import APIRouter

from app.agents.plant_health_agent import check_plant_health
from app.agents.water_management_agent import water_management
from app.services.monitor_service import MonitorData, get_monitor_data


router = APIRouter(prefix="/monitor", tags=["Monitor"])


def fetch_data() -> MonitorData:
    return get_monitor_data()


@router.get("/data")
def get_data() -> MonitorData:
    return fetch_data()


@router.get("/plant-health")
def plant_health() -> dict[str, str]:
    data = fetch_data()
    return check_plant_health(data)


@router.get("/water-management")
def water_manage() -> dict[str, str]:
    data = fetch_data()
    return water_management(data)
