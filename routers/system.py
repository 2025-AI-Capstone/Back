from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from sqlalchemy import desc
from sqlalchemy.orm import aliased
from sqlalchemy import func

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
    # 서브쿼리: 각 node_name별로 가장 큰 id값(=가장 최신 상태)을 찾음
    subq = (
        db.query(
            models.SystemStatus.node_name,
            func.max(models.SystemStatus.id).label("max_id")
        )
        .group_by(models.SystemStatus.node_name)
        .subquery()
    )

    # 메인쿼리: 서브쿼리에서 구한 id(max_id)로 실제 레코드를 가져옴
    latest_statuses = (
        db.query(models.SystemStatus)
        .join(subq, models.SystemStatus.id == subq.c.max_id)
        .all()
    )

    return latest_statuses