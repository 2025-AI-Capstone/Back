from fastapi import HTTPException, Response, Cookie, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import uuid4

from database import get_db
import models

# ────────────── 세션 저장소 ──────────────
session_store = {}

# ────────────── 스키마 ──────────────
class LoginRequest(BaseModel):
    name: str
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: int

# ────────────── 로그인 API ──────────────
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == request.name).first()
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="잘못된 로그인 정보입니다.")

    session_id = str(uuid4())
    session_store[session_id] = user.id
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    return {"message": "로그인 성공", "user_id": user.id}

# ────────────── 로그인된 사용자 확인 API ──────────────
def get_user(session_id: str = Cookie(None)):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid or expired")
    return {"user_id": session_store[session_id]}
