from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter()

# ────────────── 시스템 상태 생성 ──────────────
@router.post("/system-statuses", response_model=schemas.SystemStatusResponse)
def create_system_status(
    system: schemas.SystemStatusCreate,
    db: Session = Depends(get_db)
):
    new_system = models.SystemStatus(**system.model_dump())
    db.add(new_system)
    db.commit()
    db.refresh(new_system)
    return new_system

# ────────────── 전체 시스템 상태 조회 ──────────────
@router.get("/system-statuses", response_model=list[schemas.SystemStatusResponse])
def get_system_statuses(
    db: Session = Depends(get_db)
):
    return db.query(models.SystemStatus).all()
