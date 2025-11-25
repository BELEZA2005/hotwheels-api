from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("\n=== TESTE 1: Criar Cliente ===")
payload_cliente = {
    "nome": "Teste Cliente",
    "cpf": "99999999900",
    "telefone": "61900000000",
    "email": "teste@ex.com"
}
r1 = client.post("/clientes/", json=payload_cliente)
print("Status:", r1.status_code)
print("Resposta:", r1.text)


print("\n=== TESTE 2: Listar Clientes ===")
r2 = client.get("/clientes/")
print("Status:", r2.status_code)
print("Resposta:", r2.text)


print("\n=== TESTE 3: Criar Produto ===")
payload_produto = {
    "marca": "MarcaX",
    "modelo": "ModelY",
    "medida": "200/50R17",
    "preco": 123.45,
    "quantidade": 10
}
r3 = client.post("/produtos/", json=payload_produto)
print("Status:", r3.status_code)
print("Resposta:", r3.text)


print("\n=== TESTE 4: Criar Venda ===")
payload_venda = {
    "cliente_id": 1,
    "vendedor": "Vendedor Teste",
    "itens": [
        {"produto_id": 1, "quantidade": 2, "preco_unitario": 123.45}
    ]
}
r4 = client.post("/vendas/", json=payload_venda)
print("Status:", r4.status_code)
print("Resposta:", r4.text)


print("\n=== TESTE 5: Verificar Produto ===")
r5 = client.get("/produtos/1")
print("Status:", r5.status_code)
print("Resposta:", r5.text)
