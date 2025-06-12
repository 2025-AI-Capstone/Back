from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, time
from zoneinfo import ZoneInfo
import models, schemas
from database import get_db

router = APIRouter()

# ────────────── 오늘의 통계 조회 ──────────────
@router.get("/stats/today", response_model=schemas.DailyStatsResponse)
def get_today_stats(
    db: Session = Depends(get_db)
):
    today = datetime.now(ZoneInfo("Asia/Seoul")).date()
    start = datetime.combine(today, time.min, tzinfo=ZoneInfo("Asia/Seoul"))
    end = datetime.combine(today, time.max, tzinfo=ZoneInfo("Asia/Seoul"))

    fall_count, avg_confidence = db.query(
        func.count(models.EventLog.id),
        func.avg(models.EventLog.confidence_score)
    ).filter(
        models.EventLog.event_type == "fall",
        models.EventLog.detected_at >= start,
        models.EventLog.detected_at <= end
    ).first()

    routine_count = db.query(func.count(models.Routine.id)).filter(
        models.Routine.created_at >= start,
        models.Routine.created_at <= end
    ).scalar()

    return schemas.DailyStatsResponse(
        date=today,
        fall_event_count=fall_count,
        average_confidence_score=round(avg_confidence, 2) if avg_confidence else 0.0,
        routine_count=routine_count,
    )
