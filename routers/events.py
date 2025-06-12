from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from main import session_store
from sqlalchemy import or_

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
# GET /event-logs/chat
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
