"""Testes de listagem, paginação e filtros (CA13 a CA24).

Rastreabilidade: RF03 (listar com paginação) e RF04 (filtrar).
"""

import pytest


def ids(resposta):
    """Extrai a lista de ids de uma resposta de GET /itens."""
    return [item["id"] for item in resposta.json()["itens"]]


def criar_varios(criar_item, quantidade, **campos):
    """Cadastra vários itens e devolve a lista de ids, na ordem de criação."""
    return [
        criar_item(clube_selecao=f"Clube {numero}", **campos).json()["id"]
        for numero in range(1, quantidade + 1)
    ]


# ---------------------------------------------------------------------------
# RF03: listagem e paginação (CA13 a CA17)
# ---------------------------------------------------------------------------


def test_ca13_lista_vazia_quando_nao_ha_itens(client):
    resposta = client.get("/itens")

    assert resposta.status_code == 200
    assert resposta.json() == {"itens": [], "total": 0, "pagina": 1, "tamanho": 20}


def test_ca14_primeira_pagina_traz_20_itens_por_padrao(client, criar_item):
    criar_varios(criar_item, 25)

    resposta = client.get("/itens")

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 20
    assert corpo["total"] == 25
    assert corpo["pagina"] == 1
    assert corpo["tamanho"] == 20


def test_ca15_segunda_pagina_traz_os_5_itens_restantes(client, criar_item):
    ids_criados = criar_varios(criar_item, 25)

    resposta = client.get("/itens?pagina=2")

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 5
    assert corpo["total"] == 25
    assert corpo["pagina"] == 2
    # Os 5 restantes são os 5 mais antigos, do mais novo para o mais antigo.
    assert ids(resposta) == list(reversed(ids_criados[:5]))


@pytest.mark.parametrize(
    "parametros",
    ["tamanho=101", "tamanho=0", "pagina=0", "pagina=-1", "pagina=abc", "tamanho=abc"],
)
def test_ca16_rejeita_parametros_de_paginacao_invalidos(client, parametros):
    resposta = client.get(f"/itens?{parametros}")

    assert resposta.status_code == 422


def test_ca16_aceita_tamanho_maximo_de_100(client):
    resposta = client.get("/itens?tamanho=100")

    assert resposta.status_code == 200
    assert resposta.json()["tamanho"] == 100


def test_ca17_ordena_do_mais_recente_para_o_mais_antigo(client, criar_item):
    ids_criados = criar_varios(criar_item, 3)

    resposta = client.get("/itens")

    assert resposta.status_code == 200
    assert ids(resposta) == list(reversed(ids_criados))


# ---------------------------------------------------------------------------
# RF04: filtros (CA18 a CA24)
# ---------------------------------------------------------------------------


def test_ca18_filtra_por_tipo(client, criar_item):
    camisa_1 = criar_item(tipo="camisa").json()["id"]
    camisa_2 = criar_item(tipo="camisa").json()["id"]
    criar_item(tipo="bone")
    criar_item(tipo="chuteira")

    resposta = client.get("/itens?tipo=camisa")

    assert resposta.status_code == 200
    assert resposta.json()["total"] == 2
    assert ids(resposta) == [camisa_2, camisa_1]
    assert all(item["tipo"] == "camisa" for item in resposta.json()["itens"])


@pytest.mark.parametrize("busca", ["flam", "FLAM", "Flamengo", "engo"])
def test_ca19_filtra_clube_por_busca_parcial_sem_diferenciar_caixa(client, criar_item, busca):
    flamengo = criar_item(clube_selecao="Flamengo").json()["id"]
    criar_item(clube_selecao="Brasil")
    criar_item(clube_selecao="Fluminense")

    resposta = client.get(f"/itens?clube_selecao={busca}")

    assert resposta.status_code == 200
    assert ids(resposta) == [flamengo]


def test_ca20_filtra_por_temporada_exata(client, criar_item):
    alvo = criar_item(temporada="1998/99").json()["id"]
    criar_item(temporada="1998")
    criar_item(temporada="1999/00")

    resposta = client.get("/itens?temporada=1998/99")

    assert resposta.status_code == 200
    assert ids(resposta) == [alvo]


def test_ca21_combina_filtros_com_e_logico(client, criar_item):
    alvo = criar_item(tipo="camisa", fabricante="Adidas").json()["id"]
    criar_item(tipo="camisa", fabricante="Nike")
    criar_item(tipo="bone", fabricante="Adidas")

    resposta = client.get("/itens?tipo=camisa&fabricante=adidas")

    assert resposta.status_code == 200
    assert resposta.json()["total"] == 1
    assert ids(resposta) == [alvo]


def test_ca22_filtro_sem_correspondencia_retorna_lista_vazia(client, criar_item):
    criar_item(tipo="camisa")

    resposta = client.get("/itens?tipo=cachecol")

    assert resposta.status_code == 200
    assert resposta.json()["itens"] == []
    assert resposta.json()["total"] == 0


def test_ca23_total_conta_apenas_os_itens_filtrados(client, criar_item):
    criar_varios(criar_item, 12, tipo="camisa")
    criar_varios(criar_item, 5, tipo="bone")

    resposta = client.get("/itens?tipo=camisa&tamanho=5")

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 5
    assert corpo["total"] == 12


def test_ca24_rejeita_tipo_invalido_no_filtro(client):
    resposta = client.get("/itens?tipo=invalido")

    assert resposta.status_code == 422


def test_rf04_filtra_por_versao(client, criar_item):
    alvo = criar_item(versao="goleiro").json()["id"]
    criar_item(versao="titular")
    criar_item(versao="reserva")

    resposta = client.get("/itens?versao=goleiro")

    assert resposta.status_code == 200
    assert ids(resposta) == [alvo]
