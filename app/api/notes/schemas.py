from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteCreate(BaseModel):
    title: str
    content: str
    expires_in: Optional[int] = None

class NoteOut(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        orm_mode = True
