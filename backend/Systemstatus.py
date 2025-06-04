from fastapi import HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import cv2

import models
from database import get_db

# ────────────── 스키마 정의 ──────────────
class SystemStatusCreate(BaseModel):
    event_id: int = Field(..., example=1, description="이벤트 ID")
    node_name: str = Field(..., example="Camera", description="노드 이름")
    status: str = Field(..., example="Active", description="노드 상태")

class SystemStatusResponse(BaseModel):
    id: int
    node_name: str
    status: str
    timestamp: datetime

    class Config:
        orm_mode = True

# ────────────── 시스템 상태 기록 ──────────────
def create_system_status(
    system: SystemStatusCreate,
    db: Session = Depends(get_db)
):
    new_system = models.SystemStatus(**system.model_dump())
    db.add(new_system)
    db.commit()
    db.refresh(new_system)
    return new_system

# ────────────── 샘플 테스트용 상태 추가 ──────────────
def create_sample_system_status(
    db: Session = Depends(get_db)
):
    sample_data = [
        models.SystemStatus(event_id=1, node_name="Camera", status="Active"),
        models.SystemStatus(event_id=1, node_name="Detection", status="Running")
    ]
    db.add_all(sample_data)
    db.commit()
    return {"message": "샘플 시스템 상태 데이터"}

# ────────────── 실시간 상태 조회 (카메라 확인 포함) ──────────────
def get_real_time_system_status() -> List[SystemStatusResponse]:
    now = datetime.utcnow()

    def build_status(id: int, node_name: str, status: str):
        return SystemStatusResponse(
            id=id,
            node_name=node_name,
            status=status,
            timestamp=now
        )

    try:
        cap = cv2.VideoCapture(0)
        camera_ok = cap.isOpened()
        cap.release()
    except Exception:
        camera_ok = False

    statuses = [
        build_status(0, "카메라", "작동" if camera_ok else "비작동"),
        build_status(1, "객체 감지", "작동"),
        build_status(2, "추적", "작동")
    ]

    return statuses
