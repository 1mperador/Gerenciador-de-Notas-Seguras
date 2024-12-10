from fastapi import APIRouter, HTTPException, Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.utils import create_hash, authenticate_user, create_access_token, verify_password # Supondo que você tenha essas funções
from app.models import User, UserLogin, UserCreate, UserIn, UserOut
from app.database import SessionL

router = APIRouter()
users_db = {}

class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # Permite usar objetos ORM

def get_db():
    db = SessionL()
    try:
        yield db
    finally:
        db.close()

# @app.post("/auth/register", response_model=UserOut)
# async def register_user(user: UserIn):
#     # Simulação de criação no banco de dados
#     db_user = {"id": 1, "username": user.username}  # Exemplo de retorno do ORM
#     return db_use
@router.post("/register", response_model=UserOut)
async def register_user(user: UserIn, db: Session = Depends(get_db)):
    # Simula a criação do usuário no banco de dados
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Criando um novo usuário
    new_user = User(username=user.username, password=create_hash(user.password))  # Criptografe a senha
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Retorna o usuário recém-criado com a estrutura de UserOut
    return UserOut(id=new_user.id, username=new_user.username)
# @router.post("/register/", response_model=None)
# async def register_user(user: User):
#     # Sua lógica aqui
#     return {"message": "Usuário registrado com sucesso!"}
# @router.post("/register/", response_model=User)
# async def register_user(user: UserCreate):
#     # Substitua pela lógica real (ex.: salvar no banco de dados)
#     new_user = User(id=1, username=user.username, email=user.email, is_active=True)
#     return new_user
@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica se o usuário já existe
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Criação de um novo usuário
    hashed_password = create_hash(user.password)  # Função de hash da senha
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# @router.post("/register/", response_model=None)
# def register_user(user: User):
#     if user.username in users_db:
#         raise HTTPException(status_code=400, detail="Username already exists")
#     hashed_password = create_hash(user.password)
#     users_db[user.username] = hashed_password
#     return {"detail": "User registered successfully"}

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
