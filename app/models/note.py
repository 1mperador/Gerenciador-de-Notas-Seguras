from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from app.database.database import Base  # Assumindo que você tenha uma base de dados configurada
from typing import Optional

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)

    def __repr__(self):
        return f"Note(id={self.id}, title={self.title})"

class NoteOut(BaseModel):
    id: Optional[int]  # O ID é opcional para casos de criação ou leitura
    title: str  # Usando tipo nativo de string
    content: str  # Tipo nativo de string

    class Config:
        from_attributes = True  # Suporte para integração com SQLAlchemy


