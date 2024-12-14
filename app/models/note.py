from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from app.database import Base  # Assumindo que você tenha uma base de dados configurada

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)

    def __repr__(self):
        return f"Note(id={self.id}, title={self.title})"
