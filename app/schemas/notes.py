from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteOut(BaseModel):
    title: str
    content: str
    created_at: str
