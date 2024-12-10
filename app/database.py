from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker # orm = conversor de sql para py 

SQL = "sqlite:///./test.db"

# Configuração de engine 
engine = create_engine(
    SQL, connect_args={"check_same_thread": False} # check_same_thread é oara SQLite
)

# Sessão
SessionL = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# BAse para os modelos 
Base = declarative_base()

def get_db():
    db = SessionL()
    try:
        yield db
    finally:
        db.clone()

