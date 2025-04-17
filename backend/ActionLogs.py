from pydantic import BaseModel, Field
from datetime import datetime
from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime

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
