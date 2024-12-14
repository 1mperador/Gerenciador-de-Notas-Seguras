from passlib.context import CryptContext
from datetime import datetime
import uuid
from fastapi import HTTPException

# Configuração do passlib para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_hash(data: str) -> str:
    """
    Gera um hash seguro para a string fornecida.
    """
    return pwd_context.hash(data)

def verify_hash(data: str, hashed_data: str) -> bool:
    """
    Verifica se uma string corresponde ao hash armazenado.
    """
    return pwd_context.verify(data, hashed_data)

def generate_uuid() -> str:
    """
    Gera um UUID único.
    """
    return str(uuid.uuid4())

def verify_expiration(note_id: str, notes_db: dict) -> dict:
    """
    Verifica se uma nota já expirou e a remove do banco, se necessário.
    """
    note = notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note["expires_at"] and note["expires_at"] < datetime.utcnow():
        del notes_db[note_id]
        raise HTTPException(status_code=410, detail="Note has expired")
    return note
