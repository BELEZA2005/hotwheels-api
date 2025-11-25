from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlmodel import Session, select
from app.db.database import engine
from app.models.models import Venda, ItemVenda, Produto
from app.schemas.schemas import VendaCreate

def get_session():
    return Session(engine)

def get_venda_by_id(venda_id: int) -> Optional[Venda]:
    with get_session() as session:
        return session.get(Venda, venda_id)

def get_vendas(skip: int = 0, limit: int = 100) -> List[Venda]:
    with get_session() as session:
        stmt = select(Venda).offset(skip).limit(limit)
        return session.exec(stmt).all()

def create_venda(dto: VendaCreate) -> Dict[str, Any]:
    """
    Cria a venda, atualiza estoque e retorna um dict compatível com VendaRead.
    """
    with get_session() as session:
        
        # 1) Valida estoque antes
        for item in dto.itens:
            produto = session.get(Produto, item.produto_id)
            if not produto:
                raise ValueError(f"Produto {item.produto_id} não encontrado")
            if produto.quantidade < item.quantidade:
                raise ValueError(f"Estoque insuficiente para produto {produto.id} (disponível: {produto.quantidade})")

        # 2) Cria venda
        venda = Venda(
            cliente_id=dto.cliente_id,
            vendedor=dto.vendedor,
            data=datetime.utcnow().isoformat()
        )
        session.add(venda)
        session.flush()

        itens_response = []

        # 3) Cria itens da venda e atualiza estoque
        for item in dto.itens:
            produto = session.get(Produto, item.produto_id)

            item_venda = ItemVenda(
                venda_id=venda.id,
                produto_id=produto.id,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario
            )
            session.add(item_venda)
            session.flush()

            # atualizar estoque
            produto.quantidade -= item.quantidade
            session.add(produto)

            itens_response.append({
                "id": item_venda.id,
                "produto_id": produto.id,
                "quantidade": item.quantidade,
                "preco_unitario": item.preco_unitario
            })

        session.commit()

        # 4) Retorno final compatível com VendaRead
        return {
            "id": venda.id,
            "cliente_id": venda.cliente_id,
            "data": venda.data,
            "vendedor": venda.vendedor,
            "itens": itens_response
        }

def delete_venda(venda_id: int) -> bool:
    with get_session() as session:
        venda = session.get(Venda, venda_id)
        if not venda:
            return False
        session.delete(venda)
        session.commit()
        return True


