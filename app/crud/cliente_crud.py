from typing import List, Optional
from sqlmodel import Session, select
from app.db.database import engine
from app.models.models import Cliente
from app.schemas.schemas import ClienteCreate, ClienteUpdate


def get_session():
    return Session(engine)


def get_cliente_by_id(cliente_id: int) -> Optional[Cliente]:
    with get_session() as session:
        return session.get(Cliente, cliente_id)


def get_clientes(skip: int = 0, limit: int = 100) -> List[Cliente]:
    with get_session() as session:
        statement = select(Cliente).offset(skip).limit(limit)
        return session.exec(statement).all()


def create_cliente(dto: ClienteCreate) -> Cliente:
    cliente = Cliente(
        nome=dto.nome,
        cpf=dto.cpf,
        telefone=dto.telefone or "",
        email=dto.email or ""
    )
    with get_session() as session:
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
    return cliente


def update_cliente(cliente_id: int, dto: ClienteUpdate) -> Optional[Cliente]:
    with get_session() as session:
        cliente = session.get(Cliente, cliente_id)
        if not cliente:
            return None
        if dto.nome is not None:
            cliente.nome = dto.nome
        if dto.cpf is not None:
            cliente.cpf = dto.cpf
        if dto.telefone is not None:
            cliente.telefone = dto.telefone
        if dto.email is not None:
            cliente.email = dto.email
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
        return cliente


def delete_cliente(cliente_id: int) -> bool:
    with get_session() as session:
        cliente = session.get(Cliente, cliente_id)
        if not cliente:
            return False
        session.delete(cliente)
        session.commit()
        return True
