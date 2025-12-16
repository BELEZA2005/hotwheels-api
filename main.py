from fastapi import FastAPI
from app.db.database import create_db_and_tables

# IMPORTA OS ROUTERS COM OS NOMES CORRETOS
from app.routes import auth
from app.routes import cliente_routes
from app.routes import produto_routes
from app.routes import venda_routes

app = FastAPI()

# REGISTRA TODOS OS ROUTERS
app.include_router(auth.router)
app.include_router(cliente_routes.router)
app.include_router(produto_routes.router)
app.include_router(venda_routes.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()




