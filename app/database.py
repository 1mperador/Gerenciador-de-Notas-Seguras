from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker # orm = conversor de sql para py 

SQL = "sqlite:///./test.db"

# Configuração de engine 
engine = create_engine(
    SQL, connect_args={"check_same_thread": False} # check_same_thread é oara SQLite
)
# TODO NÃO SEI O QUE ESTA DE ERRO 
# Sessão
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# BAse para os modelos 
Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.clone()

