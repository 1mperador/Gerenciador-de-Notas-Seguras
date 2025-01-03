from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import uuid
from passlib.context import CryptContext

# Base Configurationss
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database simulation (replace with actual database)
notes_db = {}

# Models
class NoteIn(BaseModel):
    title: str
    content: str
    expires_in: Optional[int] = None  # Expiration time in minutes

class NoteOut(BaseModel):
    id: str
    title: str
    created_at: datetime
    expires_at: Optional[datetime]

# Utility Functions
def create_hash(data: str) -> str:
    return pwd_context.hash(data)

def verify_expiration(note_id: str):
    note = notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note["expires_at"] and note["expires_at"] < datetime.utcnow():
        del notes_db[note_id]
        raise HTTPException(status_code=410, detail="Note has expired")
    return note

# Routes
@app.post("/notes/", response_model=NoteOut)
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

@app.get("/notes/{note_id}")
def get_note(note_id: str):
    note = verify_expiration(note_id)
    return {
        "id": note_id,
        "title": note["title"],
        "created_at": note["created_at"],
        "expires_at": note["expires_at"]
    }

@app.delete("/notes/{note_id}")
def delete_note(note_id: str):
    note = notes_db.pop(note_id, None)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"detail": "Note deleted successfully"}
