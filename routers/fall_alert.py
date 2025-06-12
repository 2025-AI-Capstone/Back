from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from std_srvs.srv import SetBool, Trigger
import rclpy
from rclpy.node import Node
import time

router = APIRouter()

class ToggleFallAlertRequest(BaseModel):
    enabled: bool  # True: 알림 켜기, False: 알림 끄기

def get_temp_node():

    rclpy.init(args=None)
    return rclpy.create_node('fall_alert_toggle_node')

@router.post("/toggle-fall-alert")
def toggle_fall_alert(req: ToggleFallAlertRequest):
    node = get_temp_node()
    client = node.create_client(SetBool, 'falldetector/enable_alert')

    if not client.wait_for_service(timeout_sec=2.0):
        node.destroy_node()
        raise HTTPException(status_code=503, detail="Fall alert service unavailable")

    request = SetBool.Request()
    request.data = req.enabled

    future = client.call_async(request)
    rclpy.spin_until_future_complete(node, future)

    if future.result() is None:
        node.destroy_node()
        raise HTTPException(status_code=500, detail="No response from service")

    result = future.result()
    node.destroy_node()

    return {
        "success": result.success,
        "message": result.message,
        "enabled": req.enabled
    }

@router.get("/fall-alert/status")
def get_fall_alert_status():
    try:
        rclpy.init(args=None)
    except RuntimeError:
        pass  # 이미 초기화됐을 수 있음

    node = rclpy.create_node('fall_alert_status_client')
    client = node.create_client(Trigger, 'fall_alert/get_alert_status')

    if not client.wait_for_service(timeout_sec=2.0):
        node.destroy_node()
        raise HTTPException(status_code=503, detail="Fall alert status service unavailable")

    request = Trigger.Request()
    future = client.call_async(request)
    rclpy.spin_until_future_complete(node, future)

    if future.result() is None:
        node.destroy_node()
        raise HTTPException(status_code=500, detail="No response from service")

    result = future.result()
    node.destroy_node()

    return {
        "enabled": (result.message == "enabled")
    }
