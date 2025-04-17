from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import List

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
