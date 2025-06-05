from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from datetime import time
import models, schemas
from database import get_db
from main import session_store

router = APIRouter()

# ────────────── 루틴 생성 ──────────────
@router.post("/routines", response_model=schemas.RoutineResponse)
def create_routine(
    routine: schemas.RoutineCreate,
    db: Session = Depends(get_db),
    session_id: str = Cookie(None)
):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")

    alarm_time_only = routine.alarm_time
    routine_obj = models.Routine(
        user_id=session_store[session_id],
        title=routine.title,
        description=routine.description,
        alarm_time=alarm_time_only,
        repeat_type=routine.repeat_type
    )
    db.add(routine_obj)
    db.commit()
    db.refresh(routine_obj)
    return routine_obj

# ────────────── 내 루틴 조회 ──────────────
@router.get("/routines/me", response_model=list[schemas.RoutineResponse])
def get_my_routines(
    db: Session = Depends(get_db),
    session_id: str = Cookie(None)
):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")
    return db.query(models.Routine).filter(
        models.Routine.user_id == session_store[session_id]
    ).all()
