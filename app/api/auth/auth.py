# auth.py
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.models.user import User
from app.utils import verify_hash
from app.utils.verify import verify_hash
from auth import UserCreate, UserOut



SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def authenticate_user(username: str, password: str, db: Session):
    """
    Autentica um usuário no banco de dados.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_hash(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta):
    """
    Cria um token JWT com expiração.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
