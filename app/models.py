from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

# Modelos Pydantic
class NoteIn(BaseModel):
    title: str
    content: str
    expires_in: Optional[int] = None

class NoteOut(BaseModel):
    id: str
    title: str
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        orm_mode = True  # Permite conversão automática de objetos ORM para Pydantic

class UserBase(BaseModel):
    username: str
    email: EmailStr


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

class UserCreate(UserBase):
    password: str  # Adicionado para criação de usuário

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True  # Permite conversão automática de objetos ORM para Pydantic

# Modelos SQLAlchemy
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
