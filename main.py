from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, User
import schemas
from models import EventLog
from schemas import EventLogCreate, EventLogResponse


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, phone=user.phone)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 이벤트 로그 
@app.post("/event-logs", response_model=EventLogResponse)
def create_event_log(event: EventLogCreate, db: Session = Depends(get_db)):
    new_log = EventLog(
        user_id=event.user_id,
        event_type=event.event_type,
        status=event.status,
        confidence_score=event.confidence_score,
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@app.get("/event-logs/user/{user_id}", response_model=list[EventLogResponse])
def get_user_event_logs(user_id: int, db: Session = Depends(get_db)):
    logs = db.query(EventLog).filter(EventLog.user_id == user_id).all()
    if not logs:
        raise HTTPException(status_code=404, detail="이벤트 로그 없음")
    return logs

