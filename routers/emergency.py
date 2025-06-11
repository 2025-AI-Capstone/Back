from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from main import session_store

router = APIRouter()

# ────────────── 긴급 연락처 생성 ──────────────
@router.post("/emergency-contacts", response_model=schemas.EmergencyContactResponse)
def create_emergency_contact(
    data: schemas.EmergencyContactCreate,
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

# ────────────── 긴급 연락처 조회 ──────────────
@router.get("/emergency-contacts/me", response_model=list[schemas.EmergencyContactResponse])
def get_my_contacts(
    db: Session = Depends(get_db),
    session_id: str = Cookie(None)
):
    if session_id not in session_store:
        raise HTTPException(status_code=401, detail="Session invalid")
    return db.query(models.EmergencyContact).filter(
        models.EmergencyContact.user_id == session_store[session_id]
    ).all()

# ────────────── 긴급 연락처 수정 ──────────────
@router.put("/emergency-contacts/{contact_id}", response_model=schemas.EmergencyContactResponse)
def update_emergency_contact(
    contact_id: int,
    data: schemas.EmergencyContactUpdate,
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

# ────────────── 긴급 연락처 삭제 ──────────────
@router.delete("/emergency-contacts/{contact_id}")
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

from utils.solapi_sms import send_sms

@router.post("/emergency/send-alert")
def send_emergency_alert(
    req: schemas.AlertRequest,
    db: Session = Depends(get_db)
):
    contacts = db.query(models.EmergencyContact).all()
    if not contacts:
        raise HTTPException(status_code=404, detail="No emergency contacts found")

    results = []
    for contact in contacts:
        res = send_sms(contact.phone, req.message)
        results.append({"phone": contact.phone, "result": res})
    return {"results": results}
