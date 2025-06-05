from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from main import session_store

router = APIRouter()

# ────────────── 이벤트 로그 생성 ──────────────
@router.post("/event-logs", response_model=schemas.EventLogResponse)
def create_event_log(
    event: schemas.EventLogCreate,
    db: Session = Depends(get_db),
    session_id: str = Cookie(None)
):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")

    log = models.EventLog(user_id=session_store[session_id], **event.dict())
    db.add(log)
    db.commit()
    db.refresh(log)

    # 액션 자동 추가
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
            status=300.0
        ))
    elif log.event_type == "tracking":
        action_logs.append(models.ActionLog(
            event_id=log.id,
            action_type="tracking_time",
            triggered_by="system",
            status=180.0
        ))

    if action_logs:
        db.add_all(action_logs)
        db.commit()

    return log

# ────────────── 내 이벤트 로그 전체 ──────────────
@router.get("/event-logs/me", response_model=list[schemas.EventLogResponse])
def get_my_event_logs(
    db: Session = Depends(get_db),
    session_id: str = Cookie(None)
):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")
    return db.query(models.EventLog).filter(
        models.EventLog.user_id == session_store[session_id]
    ).all()

# ────────────── 채팅 메시지 로그만 조회 ──────────────
@router.get("/event-logs/chat", response_model=list[schemas.EventLogResponse])
def get_chat_logs(
    db: Session = Depends(get_db),
    session_id: str = Cookie(None)
):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")
    return db.query(models.EventLog).filter(
        models.EventLog.user_id == session_store[session_id],
        models.EventLog.message.isnot(None)
    ).all()

# ────────────── 액션 로그 수동 생성 ──────────────
@router.post("/action-logs", response_model=schemas.ActionLogResponse)
def create_action_log(
    log: schemas.ActionLogCreate,
    db: Session = Depends(get_db)
):
    action = models.ActionLog(**log.dict())
    db.add(action)
    db.commit()
    db.refresh(action)
    return action

# ────────────── 이벤트 ID 기준 액션 로그 조회 ──────────────
@router.get("/action-logs/event/{event_id}", response_model=list[schemas.ActionLogResponse])
def get_action_logs(
    event_id: int,
    db: Session = Depends(get_db)
):
    logs = db.query(models.ActionLog).filter(models.ActionLog.event_id == event_id).all()
    if not logs:
        raise HTTPException(status_code=404, detail="액션 로그 없음")
    return logs
