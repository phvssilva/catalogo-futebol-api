"""Configuração compartilhada dos testes.

Este arquivo é lido automaticamente pelo pytest. Ele prepara:
- um banco de dados SQLite em memória, novo e vazio para CADA teste;
- um "client" que simula um cliente HTTP chamando a API;
- funções auxiliares para montar e cadastrar itens de exemplo.

Nenhum teste usa o banco de desenvolvimento.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app import models  # noqa: F401  (garante que a tabela Item seja registrada)
from app.database import get_session
from app.main import app

# Item completo e válido, usado como base pelos testes.
PAYLOAD_COMPLETO = {
    "tipo": "camisa",
    "clube_selecao": "Brasil",
    "temporada": "1998",
    "fabricante": "Nike",
    "patrocinador": "Brahma",
    "versao": "titular",
    "tamanho": "G",
    "condicao": "excelente",
    "observacoes": "Camisa original, comprada em 2010.",
    "foto_url": "https://exemplo.com/fotos/brasil-1998.jpg",
}


@pytest.fixture
def engine():
    """Banco SQLite em memória, criado do zero para cada teste."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def client(engine):
    """Cliente HTTP de teste, ligado ao banco em memória.

    Troca a dependência de sessão da API (get_session) por uma que usa o
    banco de teste. Ao final, a troca é desfeita.
    """

    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def payload_completo():
    """Devolve uma cópia nova do item completo (pode ser alterada à vontade)."""
    return dict(PAYLOAD_COMPLETO)


@pytest.fixture
def criar_item(client):
    """Devolve uma função que cadastra um item via POST /itens.

    Uso: resposta = criar_item(clube_selecao="Flamengo", tipo="bone")
    Os campos informados substituem os do item completo de exemplo.
    """

    def _criar(**campos):
        payload = {**PAYLOAD_COMPLETO, **campos}
        return client.post("/itens", json=payload)

    return _criar
