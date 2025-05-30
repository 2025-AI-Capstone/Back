# CapStone - Backend

"이 프로젝트는 AI 캡스톤 과제를 위한 백엔드를 맡은 코드입니다.
현재 사용자 등록, 이벤트 로그, 루틴 관리, 액션 로그, 노드 상태 등을
기록한 상태입니다."

## 프로젝트 구성

| 기능 모듈        | 설명 |
| 사용자(User)        | 사용자 등록 및 조회 |
| 로그인(login)       | 로그인 |
| 이벤트 로그(EventLog)| 낙상/이상행동 등 이벤트 기록 |
| 루틴(Routine)       | 정해진 시간의 일상 알림 등록 (예: 복약, 운동) |
| 액션 로그(ActionLog) | 외부 알림 수행 기록 |
| 시스템 상태(SystemStatus) | 카메라, 객체감지, 추적 상태 확인 |
| 오늘의 통계(stats/today) | 날짜, 쓰러짐 횟수, 정확도, 루틴수 조회|
#25myproject
 main.py # 서버 실행 진입점
 models.py # SQLAlchemy ORM 모델 정의
 schemas.py # Pydantic 스키마 정의
 database.py # DB 세션 설정
 README.md # 프로젝트 설명 문서
 requirements.txt # 의존성 패키지 목록
 alembic # 마이그레이션 폴더
 alembic/versions # 마이그레이션 히스토리
---

eventlog
-> event_type : 이벤트 발생시 이벤트의 종류 
actionlog type
routinelog type

systemStatus  작동 비작동

##  실행 방법

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows 기준

# 패키지 설치
pip install -r requirements.txt

# 데이터베이스 초기화
alembic upgrade head

# 서버 실행
uvicorn main:app --reload

#Swagger문서 등록 조회 링크
http://127.0.0.1:8000/docs   # Swagger 문서 