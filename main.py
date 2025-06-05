from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from core.session import session_store
from routers import (
    auth,
    users,
    emergency,
    events,
    routines,
    system,
    stats
)

init_db()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(emergency.router)
app.include_router(events.router)
app.include_router(routines.router)
app.include_router(system.router)
app.include_router(stats.router)
