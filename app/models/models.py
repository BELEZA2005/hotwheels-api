from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


# -------------------------
# MODELO DE USUÁRIO (LOGIN)
# -------------------------
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password_hash: str


# -------------------------
# MODELO DE CLIENTE
# -------------------------
class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    cpf: str
    telefone: str
    email: str


# -------------------------
# MODELO DE PRODUTO
# -------------------------
class Produto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    marca: str
    modelo: str
    medida: str
    preco: float
    quantidade: int

    itens_venda: List["ItemVenda"] = Relationship(back_populates="produto")


# -------------------------
# MODELO DE VENDA
# -------------------------
class Venda(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id")
    data: str
    vendedor: str

    itens: List["ItemVenda"] = Relationship(back_populates="venda")


# -------------------------
# MODELO RELACIONAL ITEMVENDA
# -------------------------
class ItemVenda(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    venda_id: int = Field(foreign_key="venda.id")
    produto_id: int = Field(foreign_key="produto.id")
    quantidade: int
    preco_unitario: float

    venda: Optional[Venda] = Relationship(back_populates="itens")
    produto: Optional[Produto] = Relationship(back_populates="itens_venda")
