from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modelos de Notas
class NoteIn(BaseModel):
    title: str
    content: str
    expires_in: Optional[int] = None

class NoteOut(BaseModel):
    id: str
    title: str
    created_at: datetime
    expires_at: Optional[datetime]

# Modelos de Usuário e Login
class User(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
