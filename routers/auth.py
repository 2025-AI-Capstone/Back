from fastapi import APIRouter, Depends, Response, HTTPException, Cookie
from sqlalchemy.orm import Session
from uuid import uuid4

import models, schemas
from database import get_db
from main import session_store

router = APIRouter()

@router.post("/login", response_model=schemas.LoginResponse)
def login(request: schemas.LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == request.name).first()
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="잘못된 로그인 정보입니다.")
    session_id = str(uuid4())
    session_store[session_id] = user.id
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return {"message": "로그인 성공", "user_id": user.id}

@router.get("/api/user")
def get_user(session_id: str = Cookie(None)):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid or expired")
    return {"user_id": session_store[session_id]}
