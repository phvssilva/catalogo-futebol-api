"""Testes de criação, consulta, atualização e exclusão de itens.

Critérios cobertos: CA01, CA02, CA10, CA11, CA12 (marco M2) e
CA25, CA26, CA28, CA29, CA31, CA32, CA34 a CA37 (marco M4).

Rastreabilidade: RF01 (criar), RF02 (consultar), RF05 (PUT), RF06 (PATCH),
RF07 (excluir) e RF10 (datas automáticas).
"""

import time
from datetime import UTC, datetime

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


# ---------------------------------------------------------------------------
# Marco M4: atualização e exclusão
# ---------------------------------------------------------------------------

CAMPOS_DE_DATA = ("criado_em", "atualizado_em")


def como_data(texto):
    """Converte o texto de uma data da API em datetime (sem fuso = UTC)."""
    data = datetime.fromisoformat(texto)
    return data if data.tzinfo else data.replace(tzinfo=UTC)


def sem_datas(item):
    """Devolve o item sem os campos de data, para comparar o restante."""
    return {campo: valor for campo, valor in item.items() if campo not in CAMPOS_DE_DATA}


def test_ca25_put_substitui_todos_os_campos(client, criar_item):
    item_id = criar_item().json()["id"]
    novo = {
        "tipo": "chuteira",
        "clube_selecao": "Santos",
        "temporada": "2011/12",
        "fabricante": "Umbro",
        "patrocinador": "Semp Toshiba",
        "versao": "reserva",
        "tamanho": "42",
        "condicao": "nova",
        "observacoes": "Edição comemorativa.",
        "foto_url": "https://exemplo.com/fotos/santos-2011.jpg",
    }

    resposta = client.put(f"/itens/{item_id}", json=novo)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["id"] == item_id
    for campo, valor in novo.items():
        assert corpo[campo] == valor, f"campo {campo} não foi substituído"
    # A mudança precisa ter sido gravada, não só devolvida na resposta.
    consulta = client.get(f"/itens/{item_id}").json()
    for campo, valor in novo.items():
        assert consulta[campo] == valor, f"campo {campo} não foi gravado"


def test_ca26_put_sem_campo_opcional_volta_o_campo_para_null(client, criar_item):
    item_id = criar_item(fabricante="Nike").json()["id"]

    resposta = client.put(f"/itens/{item_id}", json={"tipo": "camisa", "clube_selecao": "Brasil"})

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["fabricante"] is None
    for campo in CAMPOS_OPCIONAIS:
        assert corpo[campo] is None, f"campo {campo} deveria ter voltado para null"


def test_ca28_patch_altera_apenas_o_campo_enviado(client, criar_item):
    antes = criar_item(tamanho="G").json()

    resposta = client.patch(f"/itens/{antes['id']}", json={"tamanho": "M"})

    assert resposta.status_code == 200
    depois = resposta.json()
    assert depois["tamanho"] == "M"
    esperado = {**sem_datas(antes), "tamanho": "M"}
    assert sem_datas(depois) == esperado


def test_ca29_patch_com_null_limpa_campo_opcional(client, criar_item):
    antes = criar_item(observacoes="Camisa autografada").json()

    resposta = client.patch(f"/itens/{antes['id']}", json={"observacoes": None})

    assert resposta.status_code == 200
    depois = resposta.json()
    assert depois["observacoes"] is None
    assert sem_datas(depois) == {**sem_datas(antes), "observacoes": None}


@pytest.mark.parametrize(
    "metodo, corpo",
    [
        ("put", {"tipo": "camisa", "clube_selecao": "Brasil"}),
        ("patch", {"tamanho": "M"}),
    ],
)
def test_ca31_atualizacao_renova_atualizado_em_e_preserva_criado_em(
    client, criar_item, metodo, corpo
):
    antes = criar_item().json()
    time.sleep(0.05)  # garante que o relógio avance entre a criação e a atualização

    resposta = getattr(client, metodo)(f"/itens/{antes['id']}", json=corpo)

    assert resposta.status_code == 200
    depois = resposta.json()
    assert como_data(depois["atualizado_em"]) > como_data(antes["atualizado_em"])
    assert como_data(depois["criado_em"]) == como_data(antes["criado_em"])


@pytest.mark.parametrize(
    "metodo, corpo",
    [
        ("put", {"tipo": "camisa", "clube_selecao": "Brasil"}),
        ("patch", {"tamanho": "M"}),
    ],
)
def test_ca32_atualizar_item_inexistente_retorna_404(client, metodo, corpo):
    resposta = getattr(client, metodo)("/itens/99999", json=corpo)

    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "Item não encontrado"}


def test_ca34_exclui_item_existente_e_retorna_204_sem_corpo(client, criar_item):
    item_id = criar_item().json()["id"]

    resposta = client.delete(f"/itens/{item_id}")

    assert resposta.status_code == 204
    assert resposta.content == b""


def test_ca35_item_excluido_nao_pode_mais_ser_consultado(client, criar_item):
    item_id = criar_item().json()["id"]
    client.delete(f"/itens/{item_id}")

    resposta = client.get(f"/itens/{item_id}")

    assert resposta.status_code == 404


def test_ca36_excluir_item_inexistente_retorna_404(client):
    resposta = client.delete("/itens/99999")

    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "Item não encontrado"}


def test_ca37_excluir_um_item_nao_afeta_os_demais(client, criar_item):
    primeiro = criar_item(clube_selecao="Primeiro").json()
    segundo = criar_item(clube_selecao="Segundo").json()
    terceiro = criar_item(clube_selecao="Terceiro").json()

    resposta = client.delete(f"/itens/{segundo['id']}")

    assert resposta.status_code == 204
    listagem = client.get("/itens").json()
    assert listagem["total"] == 2
    assert [item["id"] for item in listagem["itens"]] == [terceiro["id"], primeiro["id"]]
    for original in (primeiro, terceiro):
        consulta = client.get(f"/itens/{original['id']}")
        assert consulta.status_code == 200
        assert sem_datas(consulta.json()) == sem_datas(original)
