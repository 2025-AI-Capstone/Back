# CapStone - Backend

"이 프로젝트는 AI 캡스톤 과제를 위한 백엔드를 맡은 코드입니다.
현재 사용자 등록, 이벤트 로그, 루틴 관리, 액션 로그, 노드 상태 등을
기록한 상태입니다."

--------------------------------
main -> 전체 서버 실행파일
models -> SQL 모델 정의
schmas -> 요청 응답 모델 파일
database -> DB 구축 연결 파일
requirements -> 설치 파일 목록 텍스트
app.db -> 데이터베이스 파일

=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-
## 실행 방법 (패키지 설치)
- TERMILAL - 
# 패키지 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload

#확인용
http://localhost:8000/docs