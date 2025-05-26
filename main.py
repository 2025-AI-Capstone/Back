from fastapi import FastAPI, Depends, Cookie, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, time
from uuid import uuid4 
import cv2

#내부모듈
import models
import schemas
from database import  SessionLocal

# 세션 저장소
session_store = {}

app = FastAPI()

# DB 세션
def get_db():  
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 도메인(CORS설정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],       
)

# ────────────── 로그인 ──────────────
@app.post("/login", response_model=schemas.LoginResponse)
def login(request: schemas.LoginRequest, response: Response,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == request.name).first()
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="잘못된 로그인 정보입니다.")
    session_id = str(uuid4())
    session_store[session_id] = user.id
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return {"message": "로그인 성공", "user_id": user.id}

@app.get("/api/user")
def get_user(session_id: str = Cookie(None)):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid or expired")
    return {"user_id": session_store[session_id]}

# ────────────── 사용자 ──────────────
@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#수정 구현
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, data: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in data.dict().items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ────────────── 긴급 연락처 ──────────────
@app.post("/emergency-contacts", response_model=schemas.EmergencyContactResponse)
def create_emergency_contact(data: schemas.EmergencyContactCreate, db: Session = Depends(get_db), session_id: str = Cookie(None)):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")
    contact = models.EmergencyContact(user_id=session_store[session_id], **data.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

#조회
@app.get("/emergency-contacts/me", response_model=list[schemas.EmergencyContactResponse])
def get_my_contacts(db: Session = Depends(get_db), session_id: str = Cookie(None)):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")
    return db.query(models.EmergencyContact).filter(models.EmergencyContact.user_id == session_store[session_id]).all()

#수정
@app.put("/emergency-contacts/{contact_id}", response_model=schemas.EmergencyContactResponse)
def update_emergency_contact(contact_id: int, data: schemas.EmergencyContactUpdate, db: Session = Depends(get_db), session_id: str = Cookie(None)):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")
    contact = db.query(models.EmergencyContact).filter(models.EmergencyContact.id == contact_id, models.EmergencyContact.user_id == session_store[session_id]).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for field, value in data.dict().items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact
#삭제
@app.delete("/emergency-contacts/{contact_id}")
def delete_emergency_contact(contact_id: int, db: Session = Depends(get_db), session_id: str = Cookie(None)):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")
    contact = db.query(models.EmergencyContact).filter(models.EmergencyContact.id == contact_id, models.EmergencyContact.user_id == session_store[session_id]).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"message": "삭제 완료"}



# ────────────── 이벤트 로그 ──────────────
@app.post("/event-logs", response_model=schemas.EventLogResponse)
def create_event_log(event: schemas.EventLogCreate, db: Session = Depends(get_db), session_id: str = Cookie(None)):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")
    log = models.EventLog(user_id=session_store[session_id], **event.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@app.get("/event-logs/me", response_model=list[schemas.EventLogResponse])
def get_my_event_logs(db: Session = Depends(get_db), session_id: str = Cookie(None)):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")
    return db.query(models.EventLog).filter(models.EventLog.user_id == session_store[session_id]).all()

# ────────────── 루틴 ──────────────
@app.post("/routines", response_model=schemas.RoutineResponse)
def create_routine(routine: schemas.RoutineCreate, db: Session = Depends(get_db), session_id: str = Cookie(None)):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")
    routine_obj = models.Routine(user_id=session_store[session_id], **routine.dict())
    db.add(routine_obj)
    db.commit()
    db.refresh(routine_obj)
    return routine_obj

@app.get("/routines/me", response_model=list[schemas.RoutineResponse])
def get_my_routines(db: Session = Depends(get_db), session_id: str = Cookie(None)):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")
    return db.query(models.Routine).filter(models.Routine.user_id == session_store[session_id]).all()
    return routines

# ────────────── 액션 로그 ──────────────
@app.post("/action-logs", response_model=schemas.ActionLogResponse)
def create_action_log(log: schemas.ActionLogCreate, db: Session = Depends(get_db)):
    action = models.ActionLog(**log.dict())
    db.add(action)
    db.commit()
    db.refresh(action)
    return action

@app.get("/action-logs/event/{event_id}", response_model=list[schemas.ActionLogResponse])
def get_action_logs(event_id: int, db: Session = Depends(get_db)):
    logs = db.query(models.ActionLog).filter(models.ActionLog.event_id == event_id).all()
    if not logs:
        raise HTTPException(status_code=404, detail="액션 로그 없음")
    return logs

#시스템 상태
@app.post("/system-statuses", response_model=schemas.SystemStatusResponse)
def create_system_status(system: schemas.SystemStatusCreate, db: Session = Depends(get_db)):
    new_system = schemas.SystemStatus(**system.model_dump())
    db.add(new_system)
    db.commit()
    db.refresh(new_system)
    return new_system

# ────────────── 시스템 상태 (실시간 확인) ──────────────
@app.get("/system-statuses", response_model=list[schemas.SystemStatusResponse])
def get_real_time_system_status():
    statuses = []

    # 1. 카메라 확인
    try:
        cap = cv2.VideoCapture(0)
        camera_ok = cap.isOpened()
        cap.release()
    except Exception:
        camera_ok = False

    statuses.append({"node_name": "카메라", "status": "정상" if camera_ok else "비정상"})
    statuses.append({"node_name": "객체 감지", "status": "정상"})  # TODO: 연동 필요
    statuses.append({"node_name": "추적", "status": "정상"})      # TODO: 연동 필요

    return statuses

# ────────────── 오늘의 통계 ──────────────
@app.get("/stats/today", response_model=schemas.DailyStatsResponse)
def get_today_stats(db: Session = Depends(get_db)):
    today = datetime.now().date()
    start = datetime.combine(today, time.min)
    end = datetime.combine(today, time.max)

    fall_count, avg_confidence = db.query(
        func.count(models.EventLog.id),
        func.avg(models.EventLog.confidence_score)
    ).filter(
        models.EventLog.event_type == "fall",
        models.EventLog.detected_at >= start,
        models.EventLog.detected_at <= end
    ).first()

    routine_count = db.query(func.count(models.Routine.id)).filter(
        models.Routine.created_at >= start,
        models.Routine.created_at <= end
    ).scalar()

    return schemas.DailyStatsResponse(
        date=today,
        fall_event_count=fall_count,
        average_confidence_score=round(avg_confidence, 2) if avg_confidence else 0.0,
        routine_count=routine_count
    )

#──────────────────────────────────────────────────────────────────────