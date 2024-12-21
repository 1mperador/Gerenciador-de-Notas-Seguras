from app.database.database import Base
from pydantic import BaseModel, ConfigDict
from typing import Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()

# class IgnoredType:
#     pass

# class MyModel(BaseModel):
#     model_config = ConfigDict(ignored_types=(IgnoredType,))

#     _a = IgnoredType()
#     _b: int = IgnoredType()
#     _c: IgnoredType
#     _d: IgnoredType = IgnoredType()



class UserSQLAlchemy(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)

class User(BaseModel):
    id: Optional[int]  # Usando a anotação correta para um campo opcional
    username: str
    email: str

    class Config:
        orm_mode = True  # Necessário para usar com SQLAlchemy


class NoteSQLAlchemy(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

class NoteOut(BaseModel):
    title: str  # Usando a anotação correta para tipo string
    content: str  # Exemplo de outro campo com anotação

    class Config:
        from_attributes = True  # Para permitir a integração com SQLAlch

# class User(BaseModel):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     password = Column(String)
