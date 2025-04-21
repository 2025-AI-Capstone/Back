from pydantic import BaseModel
from datetime import datetime

#User
class UserCreate(BaseModel):
    name: str
    phone: str

class UserResponse(UserCreate):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


#이벤트로그그
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