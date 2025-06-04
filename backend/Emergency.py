from fastapi import HTTPException, Depends, Cookie
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models
from database import get_db

session_store = {}

# ────────────── 스키마 정의 ──────────────
class EmergencyContactCreate(BaseModel):
    name: str = Field(..., example="아빠", description="연락처 이름")
    phone: str = Field(..., example="010-xxxx-xxx5", description="전화번호")
    relation: str = Field(..., example="아빠빠", description="관계")

class EmergencyContactUpdate(BaseModel):
    name: str
    phone: str
    relation: str

class EmergencyContactResponse(BaseModel):
    id: int
    name: str
    phone: str
    relation: str

    class Config:
        orm_mode = True

# ────────────── 등록 ──────────────
def create_emergency_contact(
    data: EmergencyContactCreate,
    db: Session = Depends(get_db),
    session_id: str = Cookie(None)
):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")
    
    contact = models.EmergencyContact(user_id=session_store[session_id], **data.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

# ────────────── 내 연락처 조회 ──────────────
def get_my_contacts(
    db: Session = Depends(get_db),
    session_id: str = Cookie(None)
):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")

    return db.query(models.EmergencyContact).filter(
        models.EmergencyContact.user_id == session_store[session_id]
    ).all()

# ────────────── 수정 ──────────────
def update_emergency_contact(
    contact_id: int,
    data: EmergencyContactUpdate,
    db: Session = Depends(get_db),
    session_id: str = Cookie(None)
):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")

    contact = db.query(models.EmergencyContact).filter(
        models.EmergencyContact.id == contact_id,
        models.EmergencyContact.user_id == session_store[session_id]
    ).first()

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    for field, value in data.dict().items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact

# ────────────── 삭제 ──────────────
def delete_emergency_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    session_id: str = Cookie(None)
):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")

    contact = db.query(models.EmergencyContact).filter(
        models.EmergencyContact.id == contact_id,
        models.EmergencyContact.user_id == session_store[session_id]
    ).first()

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    db.delete(contact)
    db.commit()
    return {"message": "삭제 완료"}
