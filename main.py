from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, User, EmergencyContact, EventLog, Routine, ActionLog, NodeStatus
import schemas 
from schemas import EventLogCreate, EventLogResponse,RoutineCreate, RoutineResponse, ActionLogCreate,ActionLogResponse,NodeStatusCreate, NodeStatusResponse, EmergencyContactCreate, EmergencyContactResponse, LoginRequest


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#로그인 
@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == request.name).first()
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="잘못된 로그인 정보입니다.")
    return {"message": "로그인 성공", "user_id": user.id}

#User
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

##########