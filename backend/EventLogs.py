from fastapi import HTTPException, Depends, Cookie
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List

import models
from database import get_db

# ────────────── 세션 저장소 ──────────────
session_store = {}

# ────────────── 스키마 ──────────────
class EventLogCreate(BaseModel):
    event_type: str = Field(..., example="fall", description="이벤트 유형 (fall, tracking 등)")
    status: str = Field(..., example="unconfirmed", description="이벤트 상태")
    confidence_score: float = Field(..., example=0.5, description="AI 신뢰도")
    message: Optional[str] = Field(None, example="침대에서 떨어짐", description="텍스트 메시지 (선택)")

class EventLogResponse(BaseModel):
    id: int
    user_id: int
    event_type: str
    status: str
    confidence_score: float
    detected_at: datetime
    message: Optional[str]

    class Config:
        orm_mode = True

# ────────────── 이벤트 등록 + 액션로그 자동생성 ──────────────
def create_event_log(
    event: EventLogCreate,
    db: Session = Depends(get_db),
    session_id: str = Cookie(None)
):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")

    log = models.EventLog(user_id=session_store[session_id], **event.dict())
    db.add(log)
    db.commit()
    db.refresh(log)

    action_logs = []

    if log.event_type == "fall":
        action_logs.append(models.ActionLog(
            event_id=log.id,
            action_type="object_detected",
            triggered_by="system",
            status=1.0
        ))
        action_logs.append(models.ActionLog(
            event_id=log.id,
            action_type="tracking_time",
            triggered_by="system",
            status=300.0  # 5분
        ))

    elif log.event_type == "tracking":
        action_logs.append(models.ActionLog(
            event_id=log.id,
            action_type="tracking_time",
            triggered_by="system",
            status=180.0  # 3분
        ))

    if action_logs:
        db.add_all(action_logs)
        db.commit()

    return log

# ────────────── 내 이벤트 전체 조회 ──────────────
def get_my_event_logs(db: Session = Depends(get_db), session_id: str = Cookie(None)) -> List[EventLogResponse]:
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")

    return db.query(models.EventLog).filter(models.EventLog.user_id == session_store[session_id]).all()

# ────────────── 채팅 메시지만 필터링 ──────────────
def get_chat_logs(db: Session = Depends(get_db), session_id: str = Cookie(None)) -> List[EventLogResponse]:
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")

    return db.query(models.EventLog).filter(
        models.EventLog.user_id == session_store[session_id],
        models.EventLog.message.isnot(None)
    ).all()
