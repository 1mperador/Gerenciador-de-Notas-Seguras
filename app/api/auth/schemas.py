from pydantic import BaseModel
from typing import Optional


# Modelo para Login de Usuário
class UserLogin(BaseModel):
    username: str
    password: str


# Modelo para Retorno do Token
class Token(BaseModel):
    access_token: str
    token_type: str


# Modelo para Dados do Usuário no Token
class TokenData(BaseModel):
    username: Optional[str] = None
