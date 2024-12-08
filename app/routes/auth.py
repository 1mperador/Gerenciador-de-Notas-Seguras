from fastapi import APIRouter, HTTPException, Depends
from app.models import User, UserLogin
from app.utils import create_hash, authenticate_user, create_access_token, verify_password # Supondo que você tenha essas funções
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
users_db = {}

@router.post("/register/")
def register_user(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = create_hash(user.password)
    users_db[user.username] = hashed_password
    return {"detail": "User registered successfully"}

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Verificar o usuário e a senha
    user = await get_user(form_data.username)  # Função que busca o usuário
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Gerar o token JWT
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}