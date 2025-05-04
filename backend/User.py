from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

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
