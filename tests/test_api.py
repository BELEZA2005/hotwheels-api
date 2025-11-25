import os
import pytest
from fastapi.testclient import TestClient
from main import app
from app.db import database

# remove arquivos de banco antigos (tenta ambos nomes comuns)
for fn in ("hotwheels.db", "database.db", "db.sqlite3"):
    try:
        if os.path.exists(fn):
            os.remove(fn)
    except Exception:
        pass


@pytest.fixture(scope="module")
def client():
    # garante que as tabelas sejam criadas antes dos testes
    database.create_db_and_tables()
    with TestClient(app) as c:
        yield c


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json().get("message") and "HotWheels" in r.json()["message"]


def test_create_cliente(client):
    payload = {
        "nome": "Teste Cliente",
        "cpf": "99999999900",
        "telefone": "61900000000",
        "email": "teste@ex.com"
    }
    r = client.post("/clientes/", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert "id" in body and body["nome"] == payload["nome"]


def test_create_produto(client):
    payload = {
        "marca": "MarcaX",
        "modelo": "ModelY",
        "medida": "200/50R17",
        "preco": 123.45,
        "quantidade": 10
    }
    r = client.post("/produtos/", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert "id" in body and body["quantidade"] == payload["quantidade"]


def test_create_venda(client):
    # assume cliente id 1 e produto id 1 (criamos acima)
    payload = {
        "cliente_id": 1,
        "vendedor": "Vendedor Teste",
        "itens": [
            {"produto_id": 1, "quantidade": 2, "preco_unitario": 123.45}
        ]
    }
    r = client.post("/vendas/", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert "id" in body and body["cliente_id"] == payload["cliente_id"]


def test_produto_estoque_atualizado(client):
    # produto 1 originalmente tinha quantidade 10, vendemos 2 -> deve ficar 8
    r = client.get("/produtos/1")
    assert r.status_code == 200
    body = r.json()
    assert "quantidade" in body
    assert body["quantidade"] == 8
