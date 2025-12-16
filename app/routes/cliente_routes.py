from typing import List
from fastapi import APIRouter, HTTPException, status, Query, Depends

from app.schemas.schemas import ClienteCreate, ClienteRead, ClienteUpdate
from app.crud.cliente_crud import (
    get_clientes,
    get_cliente_by_id,
    create_cliente,
    update_cliente,
    delete_cliente,
)

# IMPORTA O OAUTH2 (ESSENCIAL PARA O AUTHORIZE)
from app.routes.auth import oauth2_scheme

router = APIRouter()


@router.get(
    "/",
    response_model=List[ClienteRead],
    tags=["Clientes"]
)
def list_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1)
):
    return get_clientes(skip=skip, limit=limit)


# 🔒 ROTA PROTEGIDA (FAZ O AUTHORIZE APARECER)
@router.get(
    "/{cliente_id}",
    response_model=ClienteRead,
    tags=["Clientes"]
)
def read_cliente(
    cliente_id: int,
    token: str = Depends(oauth2_scheme)
):
    cliente = get_cliente_by_id(cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    return cliente


@router.post(
    "/",
    response_model=ClienteRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Clientes"]
)
def create_new_cliente(dto: ClienteCreate):
    # checagem simples de CPF duplicado
    existing = [c for c in get_clientes() if c.cpf == dto.cpf]
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado"
        )
    cliente = create_cliente(dto)
    return cliente


@router.put(
    "/{cliente_id}",
    response_model=ClienteRead,
    tags=["Clientes"]
)
def edit_cliente(cliente_id: int, dto: ClienteUpdate):
    updated = update_cliente(cliente_id, dto)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    return updated


@router.delete(
    "/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Clientes"]
)
def remove_cliente(cliente_id: int):
    ok = delete_cliente(cliente_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    return None

