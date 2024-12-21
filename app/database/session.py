from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL de conexão com o banco de dados
DATABASE_URL = "sqlite:///./test.db"

# Criação do engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # Para SQLite
)

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Função de dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
