from typing import List
from fastapi import APIRouter, HTTPException, status, Query
from app.schemas.schemas import VendaCreate, VendaRead
from app.crud.venda_crud import get_vendas, get_venda_by_id, create_venda, delete_venda

router = APIRouter()

@router.get("/", response_model=List[VendaRead], tags=["Vendas"])
def list_vendas(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    return get_vendas(skip=skip, limit=limit)

@router.get("/{venda_id}", response_model=VendaRead, tags=["Vendas"])
def read_venda(venda_id: int):
    venda = get_venda_by_id(venda_id)
    if not venda:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venda não encontrada")
    return venda

@router.post("/", response_model=VendaRead, status_code=status.HTTP_201_CREATED, tags=["Vendas"])
def create_new_venda(dto: VendaCreate):
    try:
        venda = create_venda(dto)
        return venda
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{venda_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Vendas"])
def remove_venda(venda_id: int):
    ok = delete_venda(venda_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venda não encontrada")
    return None
