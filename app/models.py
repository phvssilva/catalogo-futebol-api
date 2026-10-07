from datetime import UTC, datetime

from sqlalchemy import DateTime
from sqlalchemy.engine import Dialect
from sqlalchemy.types import TypeDecorator
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(UTC)


class UTCDateTime(TypeDecorator[datetime]):
    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(
        self,
        value: datetime | None,
        _dialect: Dialect,
    ) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("A data precisa incluir um fuso horário.")
        return value.astimezone(UTC)

    def process_result_value(
        self,
        value: datetime | None,
        _dialect: Dialect,
    ) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None or value.utcoffset() is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)


class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tipo: str = Field(max_length=20)
    clube_selecao: str = Field(min_length=2, max_length=100)
    temporada: str | None = Field(default=None, max_length=9)
    fabricante: str | None = Field(default=None, max_length=50)
    patrocinador: str | None = Field(default=None, max_length=100)
    versao: str | None = Field(default=None, max_length=20)
    tamanho: str | None = Field(default=None, max_length=10)
    condicao: str | None = Field(default=None, max_length=20)
    observacoes: str | None = Field(default=None, max_length=500)
    foto_url: str | None = Field(default=None, max_length=500)
    criado_em: datetime = Field(
        default_factory=utc_now,
        sa_type=UTCDateTime(),
        nullable=False,
    )
    atualizado_em: datetime = Field(
        default_factory=utc_now,
        sa_type=UTCDateTime(),
        nullable=False,
    )
