import sys
import os
import uuid

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional


from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session


from app.models import User # Importe todos os modelos definidos 
from app.models import Note  # Certifique-se de que está correto

from app.database.session import Base, engine, get_db

from app.api.notes import notes
from app.api.auth import auth
from app.api.auth import auth_router
from app.api.notes import notes_router

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)


# Base Configurations
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Incluindo as rotas
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(notes_router, prefix="/notes", tags=["notes"])

# Database simulation (replace with actual database)
notes_db = {}


# Models
# class User(BaseModel):
#     id: int
#     name: str
#     email: str
#     is_active: bool
#     # metadata: dict = Field(default_factory=dict)  # Campo complexo
#     full_name: str | None = None

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

@app.get("/")
def read_root():
    return {"detail": "Welcome to the API"}

@app.post("/notes/", response_model=NoteOut)
def create_note(note: User):
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

@app.post("/users/", response_model=User)
async def create_user(user: User):
    return user

# @app.post("/users/", response_model=User)
# async def create_user(user: User): # TODO !Modelo com resposta 
#     return user

@app.post("/create-user")
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = create_hash(password)
    user = User(username=username, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
