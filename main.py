from fastapi import FastAPI
from app.db.database import create_db_and_tables
from app.routes.cliente_routes import router as cliente_router
from app.routes.produto_routes import router as produto_router
from app.routes.venda_routes import router as venda_router

app = FastAPI(
    title="HotWheels API",
    description="""
API do sistema HotWheels para gerenciamento de Clientes, Produtos e Vendas.

**Funcionalidades:**
- CRUD de Clientes  
- CRUD de Produtos  
- CRUD de Vendas  
- Controle automático de estoque  
- Documentação completa via Swagger  
    """,
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Rotas organizadas
app.include_router(cliente_router, prefix="/clientes", tags=["Clientes"])
app.include_router(produto_router, prefix="/produtos", tags=["Produtos"])
app.include_router(venda_router, prefix="/vendas", tags=["Vendas"])

@app.get("/")
def root():
    return {"message": "API HotWheels funcionando!"}
       # <-- e esta


