# CapStone - Backend

이 프로젝트는 AI 캡스톤 과제를 위한 백엔드 서버입니다.  
사용자 등록, 로그인, 이벤트 로그 기록, 루틴 알림 등록, 액션 로그 및 시스템 상태 확인, 통계 기능 등을 제공합니다.  
프론트엔드 연동 및 AI 감지 결과 기록을 위한 RESTful API를 제공합니다.

## 프로젝트 구조

| 파일/폴더              | 설명 |
|------------------------|------|
| `main.py`              | 서버 실행 진입점, 전체 API 구현 |
| `models.py`            | SQLAlchemy ORM 모델 정의 |
| `schemas.py`           | Pydantic 스키마 정의 |
| `database.py`          | DB 세션 관리 |
| `alembic/`             | DB 마이그레이션 도구 |
| `README.md`            | 프로젝트 설명 문서 |
| `requirements.txt`     | 의존성 패키지 목록 |

-----------------------------------------------------------------

## 주요 기능 및 엔드포인트 요약

## 로그인 및 인증

- `POST /login` : 사용자 로그인, 세션 쿠키 발급
- `GET /api/user` : 쿠키 기반 사용자 인증 정보 반환

## 사용자

- `POST /users` : 사용자 등록
- `GET /users/{user_id}` : 사용자 조회
- `PUT /users/{user_id}` : 사용자 정보 수정

## 긴급 연락처 (EmergencyContact)

- `POST /emergency-contacts` : 연락처 등록
- `GET /emergency-contacts/me` : 내 연락처 목록 조회
- `PUT /emergency-contacts/{contact_id}` : 연락처 수정
- `DELETE /emergency-contacts/{contact_id}` : 연락처 삭제

## 이벤트 로그 (EventLog)

- `POST /event-logs` : 이벤트 기록 (쓰러짐, 이상행동 등)
  - `event_type`: `"fall"` 등
  - `status`: `"detected"` 등 상태 문자열
  - `confidence_score`: 감지 신뢰도 (0.0 ~ 1.0)
  - `message`: (선택) 텍스트 메시지 (STT 결과 등)
- `GET /event-logs/me` : 내 이벤트 로그 전체 조회
- `GET /event-logs/chat` : 메시지 포함된 이벤트 로그만 조회

## 루틴 (Routine)

- `POST /routines` : 루틴 등록
  - `title`: 예) `"복약 알림"`
  - `description`: 예) `"혈압약 복용"`
  - `alarm_time`: `"08:00"`
  - `repeat_type`: `"daily"`, `"once"` 등
- `GET /routines/me` : 내 루틴 목록

## 액션 로그 (ActionLog)

- `POST /action-logs`
  - `action_type`: `"object_detected"`, `"tracking_time"` 등
  - `status`: 추적시간이면 초단위 숫자 (예: `3600.0`), 감지 횟수면 `1.0` 등
- `GET /action-logs/event/{event_id}` : 특정 이벤트에 대한 액션 로그 조회

## 시스템 상태 (SystemStatus)

- `POST /system-statuses` : 시스템 상태 수동 기록
- `GET /system-statuses` : 실시간 상태 조회 (카메라, 감지, 추적)
  - 반환: `"작동"`, `"비작동"` 상태 문자열

## 오늘의 통계

- `GET /stats/today`
  - `date`: 오늘 날짜
  - `fall_event_count`: 쓰러짐 감지 수
  - `average_confidence_score`: 평균 신뢰도
  - `routine_count`: 등록된 루틴 수
  - `object_detection_count`: 객체 감지 횟수
  - `tracking_time_hour`: 총 추적 시간 (시간 단위)

-----------------------------------------------------------------

## 타입별 설명

| 타입 (type)         | 설명 |
|---------------------|------|
| `event_type`        | `"fall"`, `"abnormal_behavior"`, `"chat"` 등 |
| `action_type`       | `"object_detected"`, `"tracking_time"` |
| `system status`     | `"작동"`, `"비작동"` |
| `repeat_type`       | `"daily"`, `"once"` 등 루틴 반복 유형 |

-----------------------------------------------------------------

## 실행 방법

```bash
# 가상환경 설정 (Windows 기준)
python -m venv .venv
.venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# Alembic 마이그레이션 반영
alembic upgrade head

# 서버 실행
uvicorn main:app --reload
```

## 문서 확인

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)