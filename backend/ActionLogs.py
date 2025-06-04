from fastapi import HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

import models
from database import get_db

# ────────────── 스키마 정의 ──────────────
class ActionLogCreate(BaseModel):
    event_id: int = Field(..., example=1, description="연결된 이벤트 ID")
    action_type: str = Field(..., example="tracking_time", description="액션 유형")
    triggered_by: str = Field(..., example="system", description="트리거 주체")
    status: float = Field(..., example=180.0, description="값 (예: 추적 시간 180초 등)")

class ActionLogResponse(BaseModel):
    id: int
    event_id: int
    action_type: str
    triggered_by: str
    timestamp: datetime
    status: float

    class Config:
        orm_mode = True

# ────────────── 액션 로그 등록 ──────────────
def create_action_log(
    log: ActionLogCreate,
    db: Session = Depends(get_db)
):
    action = models.ActionLog(**log.dict())
    db.add(action)
    db.commit()
    db.refresh(action)
    return action

# ────────────── 특정 이벤트에 대한 액션 로그 조회 ──────────────
def get_action_logs(
    event_id: int,
    db: Session = Depends(get_db)
) -> List[ActionLogResponse]:
    logs = db.query(models.ActionLog).filter(models.ActionLog.event_id == event_id).all()
    if not logs:
        raise HTTPException(status_code=404, detail="액션 로그 없음")
    return logs
