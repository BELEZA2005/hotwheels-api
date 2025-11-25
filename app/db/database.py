from sqlmodel import SQLModel, create_engine

# URL do banco (temporário, vamos mudar para Docker depois)
DATABASE_URL = "sqlite:///./hotwheels.db"

# Cria a engine
engine = create_engine(
    DATABASE_URL, echo=True
)

# Função para criar as tabelas no banco
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
