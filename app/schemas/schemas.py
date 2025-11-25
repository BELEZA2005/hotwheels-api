from typing import List, Optional
from sqlmodel import SQLModel, Field


# -------------------------
# USER (auth)
# -------------------------
class UserCreate(SQLModel):
    name: str
    email: str
    password: str


class UserRead(SQLModel):
    id: int
    name: str
    email: str


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


# -------------------------
# CLIENTE
# -------------------------
class ClienteCreate(SQLModel):
    nome: str
    cpf: str
    telefone: Optional[str] = None
    email: Optional[str] = None


class ClienteRead(SQLModel):
    id: int
    nome: str
    cpf: str
    telefone: Optional[str] = None
    email: Optional[str] = None


class ClienteUpdate(SQLModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None


# -------------------------
# PRODUTO
# -------------------------
class ProdutoCreate(SQLModel):
    marca: str
    modelo: str
    medida: str
    preco: float
    quantidade: int


class ProdutoRead(SQLModel):
    id: int
    marca: str
    modelo: str
    medida: str
    preco: float
    quantidade: int


class ProdutoUpdate(SQLModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    medida: Optional[str] = None
    preco: Optional[float] = None
    quantidade: Optional[int] = None


# -------------------------
# ITEM DE VENDA (payload)
# -------------------------
class ItemVendaCreate(SQLModel):
    produto_id: int
    quantidade: int
    preco_unitario: float


class ItemVendaRead(SQLModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: float


# -------------------------
# VENDA
# -------------------------
class VendaCreate(SQLModel):
    cliente_id: int
    vendedor: str
    itens: List[ItemVendaCreate]


class VendaRead(SQLModel):
    id: int
    cliente_id: int
    data: str
    vendedor: str
    itens: List[ItemVendaRead]
