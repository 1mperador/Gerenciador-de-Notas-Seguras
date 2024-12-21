from pydantic import BaseModel
# from app.schemas.notes import NoteCreate, NoteOut



# Classe para criar uma nova nota
class NoteCreate(BaseModel):
    title: str
    content: str

# Classe para saída (resposta) de uma nota
class NoteOut(BaseModel):
    id: int
    title: str
    content: str

    # class Config:
    #     orm_mode = True  # Isso permite que o Pydantic trabalhe com os objetos ORM do SQLAlchemy
