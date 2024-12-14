from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Note
from schemas import NoteCreate, NoteOut
from uuid import uuid4
from datetime import datetime, timedelta
from app.models.note import Note
from notes import NoteCreate, NoteOut
from app.schemas.notes import NoteCreate, NoteOut
from app.schemas.auth import UserCreate, UserOut



notes_router = APIRouter()

@notes_router.post("/", response_model=NoteOut)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    note_id = str(uuid4())
    created_at = datetime.utcnow()
    expires_at = None
    if note.expires_in:
        expires_at = created_at + timedelta(minutes=note.expires_in)
    
    new_note = Note(
        id=note_id,
        title=note.title,
        content=note.content,
        created_at=created_at,
        expires_at=expires_at
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@notes_router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: str, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@notes_router.delete("/{note_id}")
def delete_note(note_id: str, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"detail": "Note deleted successfully"}
