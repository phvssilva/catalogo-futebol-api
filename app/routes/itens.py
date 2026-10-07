from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.models import Item
from app.schemas import ItemCreate, ItemRead

router = APIRouter(prefix="/itens", tags=["itens"])


@router.post("", response_model=ItemRead, status_code=201)
def criar_item(
    dados: ItemCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Item:
    agora = datetime.now(UTC)
    item = Item(
        **dados.model_dump(exclude={"id", "criado_em", "atualizado_em"}),
        criado_em=agora,
        atualizado_em=agora,
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("/{item_id}", response_model=ItemRead)
def consultar_item(
    item_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> Item:
    item = session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item
