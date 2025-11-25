from typing import List
from fastapi import APIRouter, HTTPException, status, Query
from app.schemas.schemas import ProdutoCreate, ProdutoRead, ProdutoUpdate
from app.crud.produto_crud import (
    get_produtos,
    get_produto_by_id,
    create_produto,
    update_produto,
    delete_produto,
)

router = APIRouter()


@router.get("/", response_model=List[ProdutoRead], tags=["Produtos"])
def list_produtos(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    return get_produtos(skip=skip, limit=limit)


@router.get("/{produto_id}", response_model=ProdutoRead, tags=["Produtos"])
def read_produto(produto_id: int):
    produto = get_produto_by_id(produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return produto


@router.post("/", response_model=ProdutoRead, status_code=status.HTTP_201_CREATED, tags=["Produtos"])
def create_new_produto(dto: ProdutoCreate):
    produto = create_produto(dto)
    return produto


@router.put("/{produto_id}", response_model=ProdutoRead, tags=["Produtos"])
def edit_produto(produto_id: int, dto: ProdutoUpdate):
    updated = update_produto(produto_id, dto)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return updated


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Produtos"])
def remove_produto(produto_id: int):
    ok = delete_produto(produto_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return None
