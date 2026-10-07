"""Testes de criação e consulta de itens (CA01, CA02, CA10, CA11, CA12).

Rastreabilidade: RF01 (criar), RF02 (consultar) e RF10 (datas automáticas).
"""

import pytest

CAMPOS_OPCIONAIS = [
    "temporada",
    "fabricante",
    "patrocinador",
    "versao",
    "tamanho",
    "condicao",
    "observacoes",
    "foto_url",
]


def test_ca01_cria_item_completo(client, payload_completo):
    resposta = client.post("/itens", json=payload_completo)

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert isinstance(corpo["id"], int)
    for campo, valor in payload_completo.items():
        assert corpo[campo] == valor, f"campo {campo} diferente do enviado"
    assert corpo["criado_em"] is not None
    assert corpo["atualizado_em"] is not None
    assert corpo["criado_em"] == corpo["atualizado_em"]


def test_ca02_cria_item_apenas_com_campos_obrigatorios(client):
    resposta = client.post("/itens", json={"tipo": "bone", "clube_selecao": "Flamengo"})

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["tipo"] == "bone"
    assert corpo["clube_selecao"] == "Flamengo"
    for campo in CAMPOS_OPCIONAIS:
        assert campo in corpo, f"campo {campo} deveria aparecer na resposta"
        assert corpo[campo] is None, f"campo {campo} deveria ser null"


def test_ca10_consulta_item_existente(client, criar_item, payload_completo):
    criado = criar_item().json()

    resposta = client.get(f"/itens/{criado['id']}")

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["id"] == criado["id"]
    for campo, valor in payload_completo.items():
        assert corpo[campo] == valor, f"campo {campo} diferente do cadastrado"
    assert corpo["criado_em"] is not None
    assert corpo["atualizado_em"] is not None


def test_ca11_consulta_item_inexistente_retorna_404(client):
    resposta = client.get("/itens/99999")

    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "Item não encontrado"}


@pytest.mark.parametrize("id_invalido", ["abc", "1.5"])
def test_ca12_consulta_com_id_nao_numerico_retorna_422(client, id_invalido):
    resposta = client.get(f"/itens/{id_invalido}")

    assert resposta.status_code == 422
