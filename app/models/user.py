from app.database.database import Base
from pydantic import BaseModel, ConfigDict
from typing import Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Declarative base para SQLAlchemy
Base = declarative_base()

# Modelo SQLAlchemy
class UserSQLAlchemy(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)

# Modelo Pydantic
class User(BaseModel):
    id: Optional[int]  # Usando a anotação correta para um campo opcional
    username: str
    email: str

    class Config:
        orm_mode = True  # Necessário para usar com SQLAlchemy


# Modelo SQLAlchemy para Note
class NoteSQLAlchemy(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

# Modelo Pydantic para Note
class NoteOut(BaseModel):
    id: Optional[int]  # Adicionando ID opcional caso precise retornar com ele
    title: str  # Usando o tipo correto
    content: str

    class Config:
        from_attributes = True  # Suporte para integração com SQLAlchemy
