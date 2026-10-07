"""Testes de validação da criação de itens (CA03 a CA09).

Rastreabilidade: RF01 (criar) e RF08 (validação), regras RN02, RN04 e RN08.
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
