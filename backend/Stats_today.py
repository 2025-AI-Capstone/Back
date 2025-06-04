from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, time
from pydantic import BaseModel
import models
from database import get_db

# ────────────── 스키마 정의 ──────────────
class DailyStatsResponse(BaseModel):
    date: datetime
    fall_event_count: int
    average_confidence_score: float
    routine_count: int
    object_detection_count: int
    tracking_time_hour: float

# ────────────── 오늘의 통계 조회 ──────────────
def get_today_stats(
    db: Session = Depends(get_db)
) -> DailyStatsResponse:
    today = datetime.now().date()
    start = datetime.combine(today, time.min)
    end = datetime.combine(today, time.max)

    # 낙상 이벤트 수 + 평균 신뢰도
    fall_count, avg_confidence = db.query(
        func.count(models.EventLog.id),
        func.avg(models.EventLog.confidence_score)
    ).filter(
        models.EventLog.event_type == "fall",
        models.EventLog.detected_at >= start,
        models.EventLog.detected_at <= end
    ).first()

    # 루틴 수
    routine_count = db.query(func.count(models.Routine.id)).filter(
        models.Routine.created_at >= start,
        models.Routine.created_at <= end
    ).scalar()

    # 객체 감지 횟수
    object_detection_count = db.query(func.count(models.ActionLog.id)).filter(
        models.ActionLog.action_type == "object_detected",
        models.ActionLog.timestamp >= start,
        models.ActionLog.timestamp <= end
    ).scalar()

    # 추적 시간 합산 → 시간(시간 단위)으로 변환
    total_tracking_seconds = db.query(func.sum(models.ActionLog.status)).filter(
        models.ActionLog.action_type == "tracking_time",
        models.ActionLog.timestamp >= start,
        models.ActionLog.timestamp <= end
    ).scalar() or 0

    tracking_time_hour = round(total_tracking_seconds / 3600, 2)

    return DailyStatsResponse(
        date=today,
        fall_event_count=fall_count,
        average_confidence_score=round(avg_confidence, 2) if avg_confidence else 0.0,
        routine_count=routine_count,
        object_detection_count=object_detection_count,
        tracking_time_hour=tracking_time_hour
    )
