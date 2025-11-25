from typing import List, Optional
from sqlmodel import Session, select
from app.db.database import engine
from app.models.models import Produto
from app.schemas.schemas import ProdutoCreate, ProdutoUpdate


def get_session():
    return Session(engine)


def get_produto_by_id(produto_id: int) -> Optional[Produto]:
    with get_session() as session:
        return session.get(Produto, produto_id)


def get_produtos(skip: int = 0, limit: int = 100) -> List[Produto]:
    with get_session() as session:
        stmt = select(Produto).offset(skip).limit(limit)
        return session.exec(stmt).all()


def create_produto(dto: ProdutoCreate) -> Produto:
    produto = Produto(
        marca=dto.marca,
        modelo=dto.modelo,
        medida=dto.medida,
        preco=dto.preco,
        quantidade=dto.quantidade
    )
    with get_session() as session:
        session.add(produto)
        session.commit()
        session.refresh(produto)
    return produto


def update_produto(produto_id: int, dto: ProdutoUpdate) -> Optional[Produto]:
    with get_session() as session:
        produto = session.get(Produto, produto_id)
        if not produto:
            return None
        if dto.marca is not None:
            produto.marca = dto.marca
        if dto.modelo is not None:
            produto.modelo = dto.modelo
        if dto.medida is not None:
            produto.medida = dto.medida
        if dto.preco is not None:
            produto.preco = dto.preco
        if dto.quantidade is not None:
            produto.quantidade = dto.quantidade
        session.add(produto)
        session.commit()
        session.refresh(produto)
        return produto


def delete_produto(produto_id: int) -> bool:
    with get_session() as session:
        produto = session.get(Produto, produto_id)
        if not produto:
            return False
        session.delete(produto)
        session.commit()
        return True
