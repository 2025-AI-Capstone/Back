# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Time
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

#User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)  # 로그인 구현현
    created_at = Column(DateTime, default=datetime.utcnow)


#모델
#EmergencyContact
class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    name = Column(String)
    phone = Column(String)
    relation = Column(String)



#EventLog
class EventLog(Base):
    __tablename__ = "event_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    event_type = Column(String)
    status = Column(String)
    confidence_score = Column(Float)
    detected_at = Column(DateTime, default=datetime.utcnow)

#Routine
class Routine(Base):
    __tablename__ = "routines"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String)
    description = Column(String)
    alarm_time = Column(Time)
    repeat_type = Column(String)

#ActionLog
class ActionLog(Base):
    __tablename__ = "action_logs"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    action_type = Column(String)
    triggered_by = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

#NodeStatus
class NodeStatus(Base):
    __tablename__ = "node_statuses"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    node_name = Column(String)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
