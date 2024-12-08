from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from app.models import NoteIn, NoteOut
from app.utils import create_hash, verify_expiration
import uuid

router = APIRouter()
notes_db = {}

@router.post("/", response_model=NoteOut)
def create_note(note: NoteIn):
    note_id = str(uuid.uuid4())
    created_at = datetime.utcnow()
    expires_at = None
    
    if note.expires_in:
        expires_at = created_at + timedelta(minutes=note.expires_in)

    notes_db[note_id] = {
        "title": note.title,
        "content": create_hash(note.content),
        "created_at": created_at,
        "expires_at": expires_at
    }

    return {
        "id": note_id,
        "title": note.title,
        "created_at": created_at,
        "expires_at": expires_at
    }

@router.get("/{note_id}")
def get_note(note_id: str):
    note = verify_expiration(note_id, notes_db)
    return {
        "id": note_id,
        "title": note["title"],
        "created_at": note["created_at"],
        "expires_at": note["expires_at"]
    }

@router.delete("/{note_id}")
def delete_note(note_id: str):
    note = notes_db.pop(note_id, None)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"detail": "Note deleted successfully"}
