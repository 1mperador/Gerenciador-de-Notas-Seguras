from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_hash(data: str) -> str:
    return pwd_context.hash(data)

def authenticate_user(username: str, password: str, users_db: dict):
    hashed_password = users_db.get(username)
    if not hashed_password or not pwd_context.verify(password, hashed_password):
        return False
    return True

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

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
