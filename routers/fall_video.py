from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db, engine
from models import FallEvent, Base
from schemas import FallEventResponse, FallEventListResponse
from typing import List
import os
from datetime import datetime
import shutil
import json

router = APIRouter()

MEDIA_DIR = "media"
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

# 테이블이 없으면 생성
Base.metadata.create_all(bind=engine)

@router.post("/fall-video", response_model=FallEventResponse)
def create_fall_event(
    image: UploadFile = File(...),
    timestamp: str = Form(...),
    is_fall: bool = Form(...),
    keypoints: str = Form(...),
    bboxes: str = Form(...),
    db: Session = Depends(get_db)
):
    # 파일 저장
    try:
        dt = datetime.fromisoformat(timestamp)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")
    filename = f"fall_{dt.strftime('%Y%m%d_%H%M%S')}.jpg"
    file_path = os.path.join(MEDIA_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    # JSON 파싱
    try:
        keypoints_obj = json.loads(keypoints)
        bboxes_obj = json.loads(bboxes)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON for keypoints or bboxes")
    # DB 저장
    event = FallEvent(
        file_path=file_path,
        timestamp=dt,
        is_fall=is_fall,
        keypoints=keypoints_obj,
        bboxes=bboxes_obj
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("/fall-video", response_model=List[FallEventListResponse])
def list_fall_events(db: Session = Depends(get_db)):
    events = db.query(FallEvent).order_by(FallEvent.timestamp.desc()).all()
    return events

@router.get("/fall-video/{event_id}", response_model=FallEventResponse)
def get_fall_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(FallEvent).filter(FallEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
# StaticFiles 마운트는 main.py에서 처리
