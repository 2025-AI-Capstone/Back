from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#User
class UserCreate(BaseModel):
    name: str
    phone: str
    password: str  # 로그인 구현 패스워드드

class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    created_at: datetime

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
    user_id: int
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
    user_id: int
    event_type: str
    status: str
    confidence_score: float

class EventLogResponse(EventLogCreate):
    id: int
    detected_at: datetime

    model_config = {
        "from_attributes": True 
    }

#루틴
class RoutineCreate(BaseModel):
    user_id : int
    title : str
    description : str
    alarm_time : datetime
    repear_type : str

class RoutineResponse(RoutineCreate):
    id : int

    model_config = {
        "from_attributes": True
    }

# 액션로그
class ActionLogCreate(BaseModel):
    event_id: int
    action_type: str
    triggered_by: str

class ActionLogResponse(ActionLogCreate):
    id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }

#노드상태
class NodeStatusCreate(BaseModel):
    event_id: int
    node_name: str
    status: str

class NodeStatusResponse(NodeStatusCreate):
    id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }

class DailyStatsResponse(BaseModel):
    date: datetime
    fall_event_count: int
    average_confidence_score: Optional[float]
    routine_count: int