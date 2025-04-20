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


#EventLog
class EventLogCreate(BaseModel):
    user_id: int
    event_type: str
    status: str
    confidence_score: float

#응답
class EventLogResponse(EventLogCreate):
    id: int
    detected_at: datetime

    model_config = {
        "from_attributes": True 
    }
