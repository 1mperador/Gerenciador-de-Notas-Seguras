from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException


from sqlalchemy.orm import Session  # Importando o tipo correto de sessão

from app.utils import verify_password
from app.models import User
from app.security import verify_password

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_hash(data: str) -> str:
    return pwd_context.hash(data)

def authenticate_user(username: str, password: str, db: Session):
    # Buscar o usuário no banco de dados
    user = db.query(User).filter(User.username == username).first()  # Assumindo que você tem uma tabela User
    if not user or not verify_password(password, user.password):
        return False
    return user
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_expiration(note_id: str, notes_db: dict):
    note = notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note["expires_at"] and note["expires_at"] < datetime.utcnow():
        del notes_db[note_id]
        raise HTTPException(status_code=410, detail="Note has expired")
    return note
