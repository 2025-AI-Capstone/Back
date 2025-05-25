from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#User
class UserCreate(BaseModel):
    name: str
    phone: str
    password: str  # 로그인 구현 패스워드드

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
    information: str  # 정보 필드 추가

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
    status : str

class ActionLogResponse(ActionLogCreate):
    id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }
#대화 

#노드상태
class NodeStatusCreate(BaseModel):
    event_id: int     # X 없앨예정
    node_name: str
    status: str

class NodeStatusResponse(NodeStatusCreate):
    id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }

# 오늘의 통계 응답
class DailyStatsResponse(BaseModel):
    date: datetime                  # 날짜
    fall_event_count: int           # 쓰러짐 개수
    average_confidence_score: float = 0.0  # 기본값 0.0 
    routine_count: int              # 루틴 개수