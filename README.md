# CapStone - Backend

"이 프로젝트는 AI 캡스톤 과제를 위한 백엔드를 맡은 코드입니다.
현재 사용자 등록, 이벤트 로그, 루틴 관리, 액션 로그, 노드 상태 등을
기록한 상태입니다."

## 프로젝트 구성

| 기능 모듈        | 설명 |
|------------------|------|
| 사용자(User)        | 사용자 등록 및 조회 |
| 이벤트 로그(EventLog) | 낙상/이상행동 등 이벤트 기록 |
| 루틴(Routine)       | 정해진 시간의 일상 알림 등록 (예: 복약, 운동) |
| 액션 로그(ActionLog) | 슬랙 등 외부 알림 수행 기록 |
| 노드 상태(NodeStatus) | 센서 등의 상태 기록 |


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

#확인용
http://127.0.0.1:8000/docs   # Swagger 문서 