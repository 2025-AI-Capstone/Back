from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

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