from fastapi import FastAPI, Header, Depends, Cookie, Request, Response,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, time
from database import  SessionLocal
from uuid import uuid4 
from models import  User, EmergencyContact, EventLog, Routine, ActionLog, NodeStatus
import schemas
from schemas import EventLogCreate, EventLogResponse,RoutineCreate, RoutineResponse, ActionLogCreate,ActionLogResponse,NodeStatusCreate, NodeStatusResponse, EmergencyContactCreate, EmergencyContactResponse, LoginRequest, LoginResponse, DailyStatsResponse
from fastapi.middleware.cors import CORSMiddleware


session_store = {}

app = FastAPI()

def get_db():  
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 도메인 허용

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # origin 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용        
)
#로그인 구현 요청
@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, response: Response,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == request.name).first()
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





#User
@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name=user.name, 
        phone=user.phone,
        password = user.password
        )
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

# 긴급 연락처 등록
@app.post("/emergency-contacts", response_model=EmergencyContactResponse)
def create_emergency_contact(data: EmergencyContactCreate, db: Session = Depends(get_db)):
    contact = EmergencyContact(**data.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact



# 사용자별 연락처 조회
@app.get("/emergency-contacts/user/{user_id}", response_model=list[EmergencyContactResponse])
def get_contacts_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(EmergencyContact).filter(EmergencyContact.user_id == user_id).all()


# 긴급 연락처 삭제
@app.delete("/emergency-contact/{contact_id}")
def delete_emergency_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(EmergencyContact).filter(EmergencyContact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="연락처를 찾을 수 없습니다.")
    
    db.delete(contact)
    db.commit()
    return {"message": "삭제 되었습니다."}  

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

# 루틴
@app.post("/routines", response_model=RoutineResponse)
def create_routine(routine: RoutineCreate, db: Session = Depends(get_db)):
    new_routine = Routine(**routine.model_dump())
    db.add(new_routine)
    db.commit()
    db.refresh(new_routine)
    return new_routine

@app.get("/routines/user/{user_id}", response_model=list[RoutineResponse])
def get_user_routines(user_id: int, db: Session = Depends(get_db)):
    routines = db.query(Routine).filter(Routine.user_id == user_id).all()
    if not routines:
        raise HTTPException(status_code=404, detail="루틴 없음")
    return routines

#액션 로그
@app.post("/action-logs", response_model=ActionLogResponse)
def create_action_log(action: ActionLogCreate, db: Session = Depends(get_db)):
    new_action = ActionLog(**action.model_dump())
    db.add(new_action)
    db.commit()
    db.refresh(new_action)
    return new_action

@app.get("/action-logs/event/{event_id}", response_model=list[ActionLogResponse])
def get_action_logs(event_id: int, db: Session = Depends(get_db)):
    logs = db.query(ActionLog).filter(ActionLog.event_id == event_id).all()
    if not logs:
        raise HTTPException(status_code=404, detail="액션 로그 없음")
    return logs

#노드 상태
@app.post("/node-statuses", response_model=NodeStatusResponse)
def create_node_status(node: NodeStatusCreate, db: Session = Depends(get_db)):
    new_node = NodeStatus(**node.model_dump())
    db.add(new_node)
    db.commit()
    db.refresh(new_node)
    return new_node

@app.get("/node-statuses/event/{event_id}", response_model=list[NodeStatusResponse])
def get_node_statuses(event_id: int, db: Session = Depends(get_db)):
    nodes = db.query(NodeStatus).filter(NodeStatus.event_id == event_id).all()
    if not nodes:
        raise HTTPException(status_code=404, detail="노드 상태 없음")
    return nodes

#오늘의 통계
@app.get("/stats/today", response_model=DailyStatsResponse)
def get_today_stats(db: Session = Depends(get_db)):
    today = datetime.now().date()
    start = datetime.combine(today, time.min)
    end = datetime.combine(today, time.max)

    # 쓰러짐 감지, 신뢰도 평균
    fall_count, avg_confidence = db.query(
        func.count(EventLog.id), #쓰러짐 감지 개수
        func.avg(EventLog.confidence_score)  # 신뢰도 평균균
    ).filter(
        EventLog.event_type == "fall",
        EventLog.detected_at >= start,
        EventLog.detected_at <= end
    ).first()

    # 루틴 개수
    routine_count = db.query(func.count(Routine.id)).filter(
        Routine.created_at >= start,
        Routine.created_at <= end
    ).scalar()

    return DailyStatsResponse(
        date=today,
        fall_event_count=fall_count,
        average_confidence_score=round(avg_confidence, 2) if avg_confidence else None,
        routine_count=routine_count
    )


##########