from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time

#User
class UserCreate(BaseModel):
    name: str
    phone: str
    password: str  

# 수정 코드 구현현
class UserUpdate(BaseModel):
    name: str
    phone: str
    information: str    

class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    created_at: datetime
    information: str  

    model_config = {"from_attributes": True}

#로그인
class LoginRequest(BaseModel):
    name: str
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: int


# 긴급 연락처 요청 
class EmergencyContactCreate(BaseModel):
    name: str
    phone: str
    relation: str

#수정
class EmergencyContactUpdate(BaseModel):
    name: str
    phone: str
    relation: str

# 응답
class EmergencyContactResponse(EmergencyContactCreate):
    id: int

    model_config = {
        "from_attributes": True
    }

#이벤트로그
class EventLogCreate(BaseModel):
    event_type: str
    status: str
    confidence_score: float
    message: Optional[str] = None  

class EventLogResponse(EventLogCreate):
    id: int
    detected_at: datetime

    model_config = {
        "from_attributes": True 
    }

#루틴
class RoutineCreate(BaseModel):
    title : str
    description : str
    alarm_time : time
    repeat_type : str

class RoutineResponse(RoutineCreate):
    id : int
    created_at : datetime

    model_config = {
        "from_attributes": True
    }

# 액션로그
class ActionLogCreate(BaseModel):
    event_id: int
    action_type: str
    triggered_by: str
    status : float

class ActionLogResponse(ActionLogCreate):
    id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }


#시스템 상태


class SystemStatusCreate(BaseModel):
    node_name: str
    status: str

class SystemStatusResponse(SystemStatusCreate):
    id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }

# 오늘의 통계 응답
class DailyStatsResponse(BaseModel):
    date: datetime                  
    fall_event_count: int           
    average_confidence_score: float = 0.0   
    routine_count: int             


class AlertRequest(BaseModel):
    message: str