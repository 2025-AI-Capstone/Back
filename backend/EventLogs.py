from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

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