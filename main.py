## 모든 API 정리
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import List

####################################
######### User ##################
####################################

app = FastAPI()

# 사용자 요청
class UserCreate(BaseModel):
    name: str = Field(..., example="노경준", description="사용자 이름")
    phone: str = Field(..., example="010-3771-5801", description="전화번호")

# 사용자 응답
class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    created_at: datetime

# 저장소
users = []
user_id_counter = 1

# 사용자 등록 API
@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    global user_id_counter
    new_user = {
        "id": user_id_counter,
        "name": user.name,
        "phone": user.phone,
        "created_at": datetime.now()
    }
    users.append(new_user)
    user_id_counter += 1
    return new_user

# 사용자 ID로 조회 API
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Error")

###########################################
#########EventLogs #########################
###########################################

app = FastAPI()

# 요청
class EventLogCreate(BaseModel):
    user_id: int = Field(..., example=1, description="사용자 ID")
    event_type: str = Field(..., example="fall", description="이벤트 종류")
    status: str = Field(..., example="unconfirmed", description="이벤트 상태")
    confidence_score: float = Field(..., example=90.0, description="신뢰도 (%)")

#응답
class EventLogResponse(BaseModel):
    id: int
    user_id: int
    event_type: str
    status: str
    confidence_score: float
    detected_at: datetime

# 저장하는 곳
event_logs = []
event_id_counter = 1

# 이벤트 등록 API
@app.post("/event-logs", response_model=EventLogResponse)
async def create_event_log(event: EventLogCreate):
    global event_id_counter
    entry = {
        "id": event_id_counter,
        "user_id": event.user_id,
        "event_type": event.event_type,
        "status": event.status,
        "confidence_score": event.confidence_score,
        "detected_at": datetime.now()
    }
    event_logs.append(entry)
    event_id_counter += 1
    return entry

# 사용자별 이벤트 전체 조회 API
@app.get("/event-logs/user/{user_id}", response_model=List[EventLogResponse])
async def get_user_event_logs(user_id: int):
    logs = [log for log in event_logs if log["user_id"] == user_id]
    if not logs:
        raise HTTPException(status_code=404, detail="Error") #이벤트 없을시 코드 404
    return logs

###########################################
####### 노드 상태 ############################
############################################

app = FastAPI()

#요청
class NodeStatusCreate(BaseModel):
    event_id: int = Field(..., description="관련된 이벤트 ID")
    node_name: str = Field(..., example="sensor_1", description="노드 이름")
    status: str = Field(..., example="정상", description="노드 상태")
#응답
class NodeStatusResponse(BaseModel):
    id: int
    event_id: int
    node_name: str
    status: str
    timestamp: datetime
#저장소
node_statuses = []
node_status_id_counter = 1
#노드 API
@app.post("/node-statuses", response_model=NodeStatusResponse)
async def create_node_status(status: NodeStatusCreate):
    global node_status_id_counter
    entry = {
        "id": node_status_id_counter,
        "event_id": status.event_id,
        "node_name": status.node_name,
        "status": status.status,
        "timestamp": datetime.now()
    }
    node_statuses.append(entry)
    node_status_id_counter += 1
    return entry
#조회 API
@app.get("/node-statuses/event/{event_id}", response_model=List[NodeStatusResponse])
async def get_node_statuses_by_event(event_id: int):
    result = [s for s in node_statuses if s["event_id"] == event_id]
    if not result:
        raise HTTPException(status_code=404, detail="error")
    return result

######################################################
################# Action ######################
######################################################


app = FastAPI()
#요청
class ActionLogCreate(BaseModel):
    event_id: int = Field(..., description="관련된 이벤트 ID")
    action_type: str = Field(..., example="slack", description="유형")
    triggered_by: str = Field(..., example="AI agent", description="액션 주체")

#응답
class ActionLogResponse(BaseModel):
    id: int
    event_id: int
    action_type: str
    triggered_by: str
    timestamp: datetime

#저장소
action_logs = []
action_log_id_counter = 1

## api 구현
# 등록 API
@app.post("/action-logs", response_model=ActionLogResponse)
async def create_action_log(action: ActionLogCreate):
    global action_log_id_counter
    entry = {
        "id": action_log_id_counter,
        "event_id": action.event_id,
        "action_type": action.action_type,
        "triggered_by": action.triggered_by,
        "trimestamp": datetime.now()
    }
    action_logs.append(entry)
    action_log_id_counter += 1
    return entry

# 액션 로그 조회 API
@app.get("/action-logs/event/{event_id}", response_model=List[ActionLogResponse])
async def get_logs_by_event(event_id: int):
    logs = [log for log in action_logs if log["event_id"] == event_id]
    if not logs:
        raise HTTPException(status_code=404, detail="Error")
    return logs

####################################
################## Routine ##################
####################################

app = FastAPI()

#  요청
class RoutineCreate(BaseModel):
    user_id: int = Field(..., example=1, description="루틴을 등록할 사용자 ID")
    title: str = Field(..., example="복약 알림", description="루틴 제목")
    description: str = Field(..., example="매일 아침 9시에 약 복용", description="루틴 설명")
    alarm_time: time = Field(..., example="09:00:00", description="알람 시간")
    repeat_type: str = Field(..., example="daily", description="반복 주기 (daily)")

# 응답
class RoutineResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    alarm_time: time
    repeat_type: str
##여기까진 그냥 루틴 등록만 된 상태

# 알람 스케줄 (scheduler)
from apscheduler.schedulers.background import BackgroundScheduler
 
scheduler = BackgroundScheduler()
scheduler.start()
# 저장소
routines = []
routine_id_counter = 1

#루틴 실행 함수
def execute_routine(routine_id: int, title: str, user_id: int):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 루틴 실행(ID {routine_id}) 사용자 {user_id} - {title}")

#  등록 API
@app.post("/routines", response_model=RoutineResponse)
async def create_routine(routine: RoutineCreate):
    global routine_id_counter
    
    new_routine = {
        "id": routine_id_counter,
        "user_id": routine.user_id,
        "title": routine.title,
        "description": routine.description,
        "alarm_time": routine.alarm_time,
        "repeat_type": routine.repeat_type
    }
    routines.append(new_routine)
    # 알람 스케줄 등록
    new_id = f"routine_{routine_id_counter}"
    scheduler.add_job(
        func=execute_routine,
        trigger="cron",  #매일 반복 됨
        id=new_id,
        hour=routine.alarm_time.hour,
        minute=routine.alarm_time.minute,
        args=[routine_id_counter, routine.title, routine.user_id],
        replace_existing=False
    )
    routine_id_counter += 1
    return new_routine

# 사용자별 조회 API
@app.get("/routines/user/{user_id}", response_model=List[RoutineResponse])
async def get_user_routines(user_id: int):
    user_routines = [r for r in routines if r["user_id"] == user_id]
    if not user_routines:
        raise HTTPException(status_code=404, detail="Error")
    return user_routines

