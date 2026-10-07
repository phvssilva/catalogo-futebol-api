from datetime import datetime
from typing import Any, Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

TipoItem = Literal["camisa", "bone", "chuteira", "cachecol", "outro"]
VersaoItem = Literal["titular", "reserva", "terceira", "goleiro", "treino"]
CondicaoItem = Literal["nova", "excelente", "boa", "desgastada"]

_CAMPOS_TEXTO = (
    "tipo",
    "clube_selecao",
    "temporada",
    "fabricante",
    "patrocinador",
    "versao",
    "tamanho",
    "condicao",
    "observacoes",
    "foto_url",
)
_CAMPOS_GERADOS = ("id", "criado_em", "atualizado_em")


class ItemCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo: TipoItem
    clube_selecao: str = Field(min_length=2, max_length=100)
    temporada: str | None = Field(
        default=None,
        pattern=r"^(?:\d{4}|\d{4}/(?:\d{2}|\d{4}))$",
        max_length=9,
    )
    fabricante: str | None = Field(default=None, max_length=50)
    patrocinador: str | None = Field(default=None, max_length=100)
    versao: VersaoItem | None = None
    tamanho: str | None = Field(default=None, max_length=10)
    condicao: CondicaoItem | None = None
    observacoes: str | None = Field(default=None, max_length=500)
    foto_url: str | None = Field(default=None, max_length=500)
    id: int | None = None
    criado_em: datetime | None = None
    atualizado_em: datetime | None = None

    @model_validator(mode="before")
    @classmethod
    def normaliza_entrada(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value

        dados = value.copy()
        for campo in _CAMPOS_GERADOS:
            dados.pop(campo, None)

        for campo in _CAMPOS_TEXTO:
            texto = dados.get(campo)
            if isinstance(texto, str):
                texto = texto.strip()
                dados[campo] = texto if campo in {"tipo", "clube_selecao"} or texto else None

        return dados

    @field_validator("foto_url")
    @classmethod
    def valida_foto_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if any(character.isspace() for character in value):
            raise ValueError("A URL precisa ser válida e usar http ou https.")

        try:
            partes = urlsplit(value)
            hostname = partes.hostname
            port = partes.port
        except ValueError as error:
            raise ValueError("A URL precisa ser válida e usar http ou https.") from error

        if (
            partes.scheme not in {"http", "https"}
            or not hostname
            or (port is not None and not 0 <= port <= 65535)
        ):
            raise ValueError("A URL precisa ser válida e usar http ou https.")
        return value


class ItemPatch(ItemCreate):
    tipo: TipoItem | None = None
    clube_selecao: str | None = Field(default=None, min_length=2, max_length=100)

    @model_validator(mode="after")
    def exige_obrigatorios_nao_nulos(self) -> "ItemPatch":
        for campo in ("tipo", "clube_selecao"):
            if campo in self.model_fields_set and getattr(self, campo) is None:
                raise ValueError(f"{campo} não pode ser null.")
        return self


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: TipoItem
    clube_selecao: str
    temporada: str | None
    fabricante: str | None
    patrocinador: str | None
    versao: VersaoItem | None
    tamanho: str | None
    condicao: CondicaoItem | None
    observacoes: str | None
    foto_url: str | None
    criado_em: datetime
    atualizado_em: datetime


class ItemList(BaseModel):
    itens: list[ItemRead]
    total: int
    pagina: int
    tamanho: int
