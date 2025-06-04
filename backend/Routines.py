from fastapi import HTTPException, Depends, Cookie
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime, time
from typing import List

import models
from database import get_db

# ────────────── 세션 저장소 ──────────────
session_store = {}

# ────────────── 스키마 정의 ──────────────
class RoutineCreate(BaseModel):
    title: str = Field(..., example="아침 약 복용", description="루틴 제목")
    description: str = Field(..., example="혈압약 복용", description="루틴 설명")
    alarm_time: time = Field(..., example="08:00:00", description="알람 시간")
    repeat_type: str = Field(..., example="daily", description="반복 주기")

class RoutineResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    alarm_time: time
    repeat_type: str
    created_at: datetime

    class Config:
        orm_mode = True

# ────────────── 루틴 등록 ──────────────
def create_routine(
    routine: RoutineCreate,
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

# ────────────── 내 루틴 목록 조회 ──────────────
def get_my_routines(
    db: Session = Depends(get_db),
    session_id: str = Cookie(None)
) -> List[RoutineResponse]:
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")

    return db.query(models.Routine).filter(models.Routine.user_id == session_store[session_id]).all()
