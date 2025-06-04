from fastapi import HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime

import models
from database import get_db

# ────────────── 스키마 ──────────────
class UserCreate(BaseModel):
    name: str = Field(..., example="홍길동", description="이름")
    phone: str = Field(..., example="010-xxxx-xxxx", description="전화번호")
    password: str = Field(..., example="1234", description="비밀번호")

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

    class Config:
        orm_mode = True

# ────────────── 사용자 등록 ──────────────
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ────────────── 사용자 수정 ──────────────
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in data.dict().items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

# ────────────── 사용자 단건 조회 ──────────────
def get_user_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
