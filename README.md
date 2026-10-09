# Catálogo de Futebol API

[![CI](https://github.com/phvssilva/catalogo-futebol-api/actions/workflows/ci.yml/badge.svg)](https://github.com/phvssilva/catalogo-futebol-api/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API%20REST-009688)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green)

Micro API REST para catalogar uma coleção pessoal de artigos de futebol (camisas, bonés, chuteiras, cachecóis etc.), com cadastro, consulta, atualização, exclusão, filtros e paginação.

Projeto desenvolvido como MVP da pós-graduação em Engenharia de Software, com **desenvolvimento orientado por especificação e apoio de LLMs** em todas as etapas, desde a especificação até o código e os testes. O processo está documentado em [`docs/uso-de-llm.md`](docs/uso-de-llm.md).

## Sumário

- [Objetivo](#objetivo)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Instalação](#instalação)
- [Como executar](#como-executar)
- [Documentação da API](#documentação-da-api)
- [Exemplos de requisição](#exemplos-de-requisição)
- [Filtros e paginação](#filtros-e-paginação)
- [Como testar](#como-testar)
- [Integração contínua](#integração-contínua)
- [Desenvolvimento com apoio de LLM](#desenvolvimento-com-apoio-de-llm)
- [Limitações e trabalhos futuros](#limitações-e-trabalhos-futuros)
- [Versões](#versões)
- [Licença](#licença)

## Objetivo

Colecionadores de artigos de futebol lidam com itens que têm muitos atributos (clube, temporada, fabricante, patrocinador, versão) e pouca padronização. Esta API oferece um lugar único e padronizado para registrar e consultar a coleção, servindo também como estudo de um processo de engenharia de software com rastreabilidade entre requisitos, critérios de aceite e testes.

## Funcionalidades

- CRUD completo do recurso `Item`: criar, consultar, listar, substituir (PUT), atualizar parcialmente (PATCH) e excluir
- Listagem com filtros por tipo, clube/seleção, temporada, fabricante e versão
- Paginação e ordenação do mais recente para o mais antigo
- Validação dos dados com mensagens de erro padronizadas
- Datas de criação e atualização geradas automaticamente (UTC)
- Endpoint de saúde (`GET /health`)
- Documentação interativa gerada automaticamente (Swagger UI)

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.14 (versão usada no desenvolvimento e no CI) |
| Framework web | FastAPI |
| ORM e modelos | SQLModel (SQLAlchemy + Pydantic) |
| Banco de dados | SQLite |
| Servidor | Uvicorn |
| Testes | pytest, pytest-cov e httpx (TestClient) |
| Qualidade de código | Ruff (lint e formatação) |
| Integração contínua | GitHub Actions |

## Estrutura do repositório

```text
catalogo-futebol-api/
├── .github/workflows/ci.yml    # Pipeline de integração contínua
├── app/
│   ├── main.py                 # Aplicação FastAPI e /health
│   ├── database.py             # Conexão com o banco e sessão
│   ├── models.py               # Tabela Item
│   ├── schemas.py              # Validação de entrada e saída
│   └── routes/itens.py         # Endpoints de /itens
├── tests/
│   ├── conftest.py             # Banco em memória e cliente de teste
│   ├── test_itens_crud.py      # Criar, consultar, atualizar e excluir
│   ├── test_validacoes.py      # Regras de validação
│   ├── test_filtros.py         # Listagem, paginação e filtros
│   └── test_health.py          # Saúde e documentação
├── docs/
│   ├── ESPECIFICACAO.md        # Requisitos, contrato da API e critérios de aceite
│   └── uso-de-llm.md           # Registro do uso de LLM no projeto
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml              # Configuração do Ruff e do pytest
├── requirements.txt            # Dependências com versões fixas
└── README.md
```

## Instalação

**Pré-requisitos:** Python 3.14 e Git.

```bash
git clone https://github.com/phvssilva/catalogo-futebol-api.git
cd catalogo-futebol-api
```

Crie e ative o ambiente virtual.

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se o Windows bloquear a ativação, rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e tente de novo.

**Linux e macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar

```bash
uvicorn app.main:app --reload
```

A API fica disponível em `http://127.0.0.1:8000`. Para parar o servidor, use `Ctrl + C`.

O banco SQLite é criado automaticamente no primeiro uso, no arquivo `catalogo.db` (ignorado pelo Git). Para usar outro banco ou local, defina a variável de ambiente `DATABASE_URL`:

```powershell
$env:DATABASE_URL = "sqlite:///./outro.db"
```

```bash
export DATABASE_URL="sqlite:///./outro.db"
```

## Documentação da API

Com o servidor em execução:

| Recurso | Endereço |
|---|---|
| Swagger UI (testar clicando) | http://127.0.0.1:8000/docs |
| Especificação OpenAPI | http://127.0.0.1:8000/openapi.json |

A especificação completa, com requisitos, regras de negócio e critérios de aceite, está em [`docs/ESPECIFICACAO.md`](docs/ESPECIFICACAO.md).

### Endpoints

| Método | Rota | Descrição | Sucesso | Erros |
|---|---|---|---|---|
| POST | `/itens` | Cria um item | `201` | `422` |
| GET | `/itens` | Lista itens, com filtros e paginação | `200` | `422` |
| GET | `/itens/{id}` | Consulta um item | `200` | `404`, `422` |
| PUT | `/itens/{id}` | Substitui todos os campos de um item | `200` | `404`, `422` |
| PATCH | `/itens/{id}` | Atualiza campos de forma parcial | `200` | `404`, `422` |
| DELETE | `/itens/{id}` | Exclui um item (exclusão física) | `204` | `404` |
| GET | `/health` | Verifica a saúde da API | `200` | — |

### Campos do item

| Campo | Obrigatório | Valores e regras |
|---|---|---|
| `tipo` | **sim** | `camisa`, `bone`, `chuteira`, `cachecol`, `outro` |
| `clube_selecao` | **sim** | 2 a 100 caracteres |
| `temporada` | não | `AAAA`, `AAAA/AA` ou `AAAA/AAAA` (ex.: `1998/99`) |
| `fabricante` | não | até 50 caracteres |
| `patrocinador` | não | até 100 caracteres |
| `versao` | não | `titular`, `reserva`, `terceira`, `goleiro`, `treino` |
| `tamanho` | não | até 10 caracteres |
| `condicao` | não | `nova`, `excelente`, `boa`, `desgastada` |
| `observacoes` | não | até 500 caracteres |
| `foto_url` | não | URL `http` ou `https` |

Os campos `id`, `criado_em` e `atualizado_em` são gerados pela API. Valores enviados para eles são ignorados, e campos desconhecidos geram erro `422`.

## Exemplos de requisição

O jeito mais simples é o Swagger UI (`/docs`), com o botão **Try it out**. Os exemplos abaixo mostram o uso pela linha de comando.

### Criar um item

**Linux, macOS ou Git Bash:**

```bash
curl -X POST http://127.0.0.1:8000/itens \
  -H "Content-Type: application/json" \
  -d '{"tipo":"camisa","clube_selecao":"Brasil","temporada":"1998","fabricante":"Nike","patrocinador":"Brahma","versao":"titular","tamanho":"G","condicao":"excelente"}'
```

**Windows (PowerShell):**

```powershell
$corpo = @{
    tipo          = "camisa"
    clube_selecao = "Brasil"
    temporada     = "1998"
    fabricante    = "Nike"
    patrocinador  = "Brahma"
    versao        = "titular"
    tamanho       = "G"
    condicao      = "excelente"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/itens `
    -ContentType "application/json" -Body $corpo
```

> No PowerShell, para textos com acento (como "São Paulo"), prefira o Swagger UI, que evita problemas de codificação.

Resposta `201 Created`:

```json
{
  "id": 1,
  "tipo": "camisa",
  "clube_selecao": "Brasil",
  "temporada": "1998",
  "fabricante": "Nike",
  "patrocinador": "Brahma",
  "versao": "titular",
  "tamanho": "G",
  "condicao": "excelente",
  "observacoes": null,
  "foto_url": null,
  "criado_em": "2026-10-07T21:11:21.760562Z",
  "atualizado_em": "2026-10-07T21:11:21.760562Z"
}
```

### Listar, atualizar e excluir

```bash
# Listar camisas da Nike, 10 por página
curl "http://127.0.0.1:8000/itens?tipo=camisa&fabricante=nike&pagina=1&tamanho=10"

# Consultar o item 1
curl http://127.0.0.1:8000/itens/1

# Atualizar só o tamanho (PATCH)
curl -X PATCH http://127.0.0.1:8000/itens/1 \
  -H "Content-Type: application/json" -d '{"tamanho":"M"}'

# Excluir o item 1
curl -X DELETE http://127.0.0.1:8000/itens/1

# Verificar a saúde da API
curl http://127.0.0.1:8000/health
```

No PowerShell, use `Invoke-RestMethod` com o mesmo endereço e `-Method Get`, `Patch` ou `Delete`.

### Resposta da listagem

```json
{
  "itens": [ { "id": 1, "tipo": "camisa", "...": "..." } ],
  "total": 1,
  "pagina": 1,
  "tamanho": 10
}
```

### Erros

| Situação | Status | Corpo |
|---|---|---|
| Item inexistente | `404` | `{"detail": "Item não encontrado"}` |
| Dados inválidos (campo obrigatório ausente, valor fora do formato, campo desconhecido) | `422` | `{"detail": [{"loc": [...], "msg": "...", "type": "..."}]}` |

## Filtros e paginação

Parâmetros de `GET /itens`:

| Parâmetro | Comportamento | Padrão |
|---|---|---|
| `tipo` | Igualdade exata | — |
| `clube_selecao` | Contém o texto, sem diferenciar maiúsculas e minúsculas | — |
| `temporada` | Igualdade exata | — |
| `fabricante` | Contém o texto, sem diferenciar maiúsculas e minúsculas | — |
| `versao` | Igualdade exata | — |
| `pagina` | Número da página (≥ 1) | `1` |
| `tamanho` | Itens por página (1 a 100) | `20` |

- Filtros combinados usam **E lógico**.
- O campo `total` da resposta conta apenas os itens que passaram pelos filtros.
- A ordenação é fixa: do mais recente para o mais antigo.

## Como testar

Com o ambiente virtual ativo:

```bash
pytest
```

O comando executa os **70 testes automatizados** e mostra a cobertura de código (configurada em `pyproject.toml`). Os testes usam um banco SQLite em memória, isolado a cada teste, e nunca tocam o seu `catalogo.db`.

Verificações de qualidade:

```bash
ruff check .
ruff format --check .
```

Para exigir a cobertura mínima de 80%, como faz o CI:

```bash
pytest --cov-fail-under=80
```

Cada teste leva no nome o ID do critério de aceite que verifica (por exemplo, `test_ca25_put_substitui_todos_os_campos`), o que dá rastreabilidade entre a especificação e os testes.

## Integração contínua

A cada `push` e `pull request` na branch `main`, o GitHub Actions ([`ci.yml`](.github/workflows/ci.yml)) instala as dependências e executa:

1. `ruff check .` (lint)
2. `ruff format --check .` (formatação)
3. `pytest --cov-fail-under=80` (testes com cobertura mínima de 80%)

## Desenvolvimento com apoio de LLM

O projeto seguiu um ciclo orientado por especificação, repetido a cada marco:

1. **Especificar:** requisitos e critérios de aceite em [`docs/ESPECIFICACAO.md`](docs/ESPECIFICACAO.md).
2. **Testar primeiro:** os testes foram escritos a partir dos critérios, antes do código.
3. **Implementar:** o código foi gerado com apoio de LLM para fazer os testes passarem.
4. **Revisar:** execução local dos testes, do Ruff e teste manual no Swagger UI.
5. **Commitar:** um commit por passo lógico, no padrão Conventional Commits.
6. **Registrar:** prompts, correções e ocorrências em [`docs/uso-de-llm.md`](docs/uso-de-llm.md).

Os testes de cada marco foram validados contra uma implementação de referência descartável e, no caso de atualização e exclusão, por um teste de mutação com defeitos propositais. O registro completo, com acertos, erros e informações desatualizadas encontradas, está em [`docs/uso-de-llm.md`](docs/uso-de-llm.md).

## Limitações e trabalhos futuros

**Limitações conhecidas**

- O filtro de texto ignora maiúsculas e minúsculas, mas **não ignora acentos** (buscar `sao` não encontra `São Paulo`).
- Não há padronização dos nomes de clubes: "São Paulo" e "sao paulo" são tratados como valores diferentes.
- Sem autenticação: a API foi pensada para uso pessoal e local.
- A exclusão é física e irreversível.

**Evolução prevista**

- Cadastro assistido por IA: enviar uma foto da camisa e receber sugestões de clube, temporada, fabricante e patrocinador, com avaliação de acurácia por campo
- Busca insensível a acentos e padronização de clubes
- Upload de fotos
- Dockerfile para execução em contêiner
- Autenticação

## Versões

O histórico de mudanças está em [`CHANGELOG.md`](CHANGELOG.md). As versões publicadas ficam na página de [Releases](https://github.com/phvssilva/catalogo-futebol-api/releases).

## Licença

Distribuído sob a licença MIT. Veja o arquivo [`LICENSE`](LICENSE).


