"""Testes do endpoint de saúde e da documentação automática (CA38 e CA39).

Rastreabilidade: RF09 (health) e RNF01 (documentação OpenAPI/Swagger).
"""


def test_ca38_health_retorna_status_ok(client):
    resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_ca39_swagger_ui_esta_disponivel(client):
    resposta = client.get("/docs")

    assert resposta.status_code == 200
    assert "swagger" in resposta.text.lower()


def test_ca39_openapi_json_esta_disponivel_e_lista_as_rotas(client):
    resposta = client.get("/openapi.json")

    assert resposta.status_code == 200
    rotas = resposta.json()["paths"]
    assert "/health" in rotas
    assert "/itens" in rotas
    assert any(rota.startswith("/itens/{") for rota in rotas)
