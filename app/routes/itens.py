from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlmodel import Session, select

from app.database import get_session
from app.models import Item
from app.schemas import ItemCreate, ItemList, ItemRead, TipoItem, VersaoItem

router = APIRouter(prefix="/itens", tags=["itens"])


@router.get("", response_model=ItemList)
def listar_itens(
    session: Annotated[Session, Depends(get_session)],
    tipo: TipoItem | None = None,
    clube_selecao: str | None = None,
    temporada: str | None = None,
    fabricante: str | None = None,
    versao: VersaoItem | None = None,
    pagina: Annotated[int, Query(ge=1)] = 1,
    tamanho: Annotated[int, Query(ge=1, le=100)] = 20,
) -> ItemList:
    filtros = []
    if tipo is not None:
        filtros.append(Item.tipo == tipo)
    if clube_selecao is not None:
        filtros.append(
            func.lower(Item.clube_selecao).contains(
                clube_selecao.lower(),
                autoescape=True,
            )
        )
    if temporada is not None:
        filtros.append(Item.temporada == temporada)
    if fabricante is not None:
        filtros.append(
            func.lower(Item.fabricante).contains(
                fabricante.lower(),
                autoescape=True,
            )
        )
    if versao is not None:
        filtros.append(Item.versao == versao)

    consulta = select(Item).where(*filtros)
    total = session.exec(select(func.count()).select_from(Item).where(*filtros)).one()
    itens = session.exec(
        consulta.order_by(
            Item.criado_em.desc(),
            Item.id.desc(),
        )
        .offset((pagina - 1) * tamanho)
        .limit(tamanho)
    ).all()

    return ItemList(
        itens=itens,
        total=total,
        pagina=pagina,
        tamanho=tamanho,
    )


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
