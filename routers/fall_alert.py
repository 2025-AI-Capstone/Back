from fastapi import APIRouter
from pydantic import BaseModel
import redis

router = APIRouter()
r = redis.Redis(host='localhost', port=6379, db=0)
STATE_KEY = "fall_alert_enabled"

class ToggleFallAlertRequest(BaseModel):
    enabled: bool

@router.post("/toggle-fall-alert")
def toggle_fall_alert(req: ToggleFallAlertRequest):
    command = "enable" if req.enabled else "disable"

    # 1. Pub/Sub: ROS2에 명령 전달
    r.publish("fall_alert_toggle", command)

    # 2. 상태 저장
    r.set(STATE_KEY, "true" if req.enabled else "false")

    return {"success": True, "command": command}

@router.get("/fall-alert/status")
def get_fall_alert_status():
    val = r.get(STATE_KEY)
    if val is None:
        # 기본값: 알림 켜짐
        return {"enabled": True}
    return {"enabled": val.decode() == "true"}
