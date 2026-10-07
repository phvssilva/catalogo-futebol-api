"""Testes de validação de itens.

Critérios cobertos: CA03 a CA09 (criação, marco M2) e CA27, CA30 e CA33
(atualização, marco M4).

Rastreabilidade: RF01 (criar), RF05 (PUT), RF06 (PATCH) e RF08 (validação),
regras RN01, RN02, RN04, RN07 e RN08.
"""

import pytest


def test_ca03_rejeita_item_sem_clube_selecao(client, payload_completo):
    payload_completo.pop("clube_selecao")

    resposta = client.post("/itens", json=payload_completo)

    assert resposta.status_code == 422


@pytest.mark.parametrize("tipo_invalido", ["invalido", "camiseta"])
def test_ca04_rejeita_tipo_fora_do_enum(criar_item, tipo_invalido):
    resposta = criar_item(tipo=tipo_invalido)

    assert resposta.status_code == 422


@pytest.mark.parametrize(
    "temporada_invalida",
    ["98-99", "1998-99", "98/99", "1998/9", "1998/999", "19998", "abcd"],
)
def test_ca05_rejeita_temporada_em_formato_invalido(criar_item, temporada_invalida):
    resposta = criar_item(temporada=temporada_invalida)

    assert resposta.status_code == 422


@pytest.mark.parametrize("temporada_valida", ["2022", "1998/99", "1998/1999"])
def test_ca05_aceita_temporada_em_formato_valido(criar_item, temporada_valida):
    resposta = criar_item(temporada=temporada_valida)

    assert resposta.status_code == 201
    assert resposta.json()["temporada"] == temporada_valida


@pytest.mark.parametrize(
    "url_invalida",
    [
        "nao-e-uma-url",
        "exemplo.com/foto.jpg",
        "ftp://exemplo.com/foto.jpg",
        "javascript:alert(1)",
    ],
)
def test_ca06_rejeita_foto_url_invalida(criar_item, url_invalida):
    resposta = criar_item(foto_url=url_invalida)

    assert resposta.status_code == 422


def test_ca07_remove_espacos_nas_pontas_do_clube_selecao(client, criar_item):
    resposta = criar_item(clube_selecao="  Brasil  ")

    assert resposta.status_code == 201
    assert resposta.json()["clube_selecao"] == "Brasil"
    # Confirma que o valor salvo no banco também está sem espaços.
    consulta = client.get(f"/itens/{resposta.json()['id']}")
    assert consulta.json()["clube_selecao"] == "Brasil"


def test_ca08_ignora_id_e_datas_enviados_pelo_cliente(criar_item):
    data_falsa = "2000-01-01T00:00:00Z"

    resposta = criar_item(id=9999, criado_em=data_falsa, atualizado_em=data_falsa)

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["id"] != 9999
    assert corpo["criado_em"] != data_falsa
    assert corpo["atualizado_em"] != data_falsa


def test_ca09_rejeita_campo_desconhecido(criar_item):
    resposta = criar_item(cor_favorita="verde")

    assert resposta.status_code == 422


# ---------------------------------------------------------------------------
# Marco M4: validação na atualização
# ---------------------------------------------------------------------------

CAMPOS_DE_DATA = ("criado_em", "atualizado_em")


def sem_datas(item):
    """Devolve o item sem os campos de data, para comparar o restante."""
    return {campo: valor for campo, valor in item.items() if campo not in CAMPOS_DE_DATA}


@pytest.mark.parametrize("campo_ausente", ["clube_selecao", "tipo"])
def test_ca27_put_sem_campo_obrigatorio_retorna_422(client, criar_item, campo_ausente):
    antes = criar_item().json()
    corpo = {"tipo": "bone", "clube_selecao": "Santos"}
    corpo.pop(campo_ausente)

    resposta = client.put(f"/itens/{antes['id']}", json=corpo)

    assert resposta.status_code == 422
    depois = client.get(f"/itens/{antes['id']}").json()
    assert sem_datas(depois) == sem_datas(antes), "o item não deveria ter sido alterado"


@pytest.mark.parametrize("campo_obrigatorio", ["clube_selecao", "tipo"])
def test_ca30_patch_nao_pode_limpar_campo_obrigatorio(client, criar_item, campo_obrigatorio):
    antes = criar_item().json()

    resposta = client.patch(f"/itens/{antes['id']}", json={campo_obrigatorio: None})

    assert resposta.status_code == 422
    depois = client.get(f"/itens/{antes['id']}").json()
    assert sem_datas(depois) == sem_datas(antes), "o item não deveria ter sido alterado"


@pytest.mark.parametrize(
    "corpo_invalido",
    [
        {"tipo": "xyz"},
        {"temporada": "98-99"},
        {"foto_url": "nao-e-uma-url"},
    ],
)
def test_ca33_patch_com_valor_invalido_retorna_422_sem_alterar_o_item(
    client, criar_item, corpo_invalido
):
    antes = criar_item().json()

    resposta = client.patch(f"/itens/{antes['id']}", json=corpo_invalido)

    assert resposta.status_code == 422
    depois = client.get(f"/itens/{antes['id']}").json()
    assert sem_datas(depois) == sem_datas(antes), "o item não deveria ter sido alterado"
