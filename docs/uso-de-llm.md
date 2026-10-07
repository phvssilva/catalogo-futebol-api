# Registro de uso de LLM

Este documento registra como o LLM foi usado no desenvolvimento da **Catálogo de Futebol API**: prompts enviados, resultados obtidos, correções feitas pelo autor, ocorrências e limitações observadas. Ele é a evidência do processo de desenvolvimento assistido por LLM.

> **Última atualização:** 2026-10-07 (marcos M2 a M5 concluídos, CI verde). Campos marcados com **`[preencher]`** dependem de informação que só o autor tem.

## 1. Informações gerais

| Item | Descrição |
|---|---|
| Autor | [preencher] |
| Ferramentas | Claude (Anthropic) em chat (claude.ai) e um agente de IA integrado ao VS Code |
| Modelo(s) | [preencher: confirmar o modelo do chat e o do agente do VS Code] |
| Ambiente | Windows, PowerShell, VS Code, Python 3.14.8 |
| Perfil do autor | Não programador. Dependência alta do LLM para código, testes e comandos |
| Abordagem | Desenvolvimento orientado por especificação (spec → testes → código → revisão → commit) |
| Documento de referência | `docs/ESPECIFICACAO.md` |

### 1.1 Divisão de papéis

| Papel | Quem executou |
|---|---|
| Planejamento, especificação, roteiro e prompts | Claude (chat) |
| Escrita dos testes | Claude (chat) |
| Validação dos testes antes da entrega | Claude (chat), em ambiente próprio, com implementação de referência descartável (não entregue ao autor) |
| Implementação do código da API | Agente do VS Code, a partir dos prompts preparados no chat |
| Execução de comandos, revisão, testes manuais e commits | Autor |

## 2. Metodologia de registro

Para cada interação relevante, registra-se: objetivo, prompt, resultado, correções do autor, avaliação e commit relacionado.

| Código | Significado |
|---|---|
| ✅ Acerto | Resultado usado sem alterações |
| 🔧 Ajuste | Resultado usado após correção ou complemento |
| ❌ Erro | Resultado incorreto, descartado ou refeito |
| 👻 Alucinação | Biblioteca, comando, parâmetro ou fato inexistente ou desatualizado |

### 2.1 Como os testes foram validados antes de chegar ao autor

Para reduzir rodadas de erro, os testes de cada marco foram executados pelo LLM contra uma **implementação de referência descartável**, escrita só para validação e não entregue. Resultados:

- Marcos M2 a M5: todos os testes passaram com a implementação de referência e o `ruff` aprovou os arquivos de teste.
- Marco M4: foram introduzidos **3 defeitos de propósito** (PUT que não zera campos omitidos, PATCH que não renova `atualizado_em`, DELETE que apaga todos os itens). Os testes detectaram os três (CA26, CA31 e CA37), o que indica que não são vazios.

---

## 3. Registro de interações

### Interação 01: Definição do tema e da abordagem

| | |
|---|---|
| **Data** | 2026-10-06 |
| **Fase** | Planejamento |
| **Objetivo** | Definir o tema do projeto e o tipo de aplicação |
| **Commit relacionado** | — (planejamento, sem código) |

**Prompt (resumo):**
> Preciso fazer um MVP de um projeto de pós-graduação em Engenharia de Software com a utilização de IA. Minha ideia é criar um catálogo da minha coleção de camisas e artigos de futebol. Qual tipo de aplicação você sugere? Quero um projeto simples, mas que atenda a todas as diretrizes de um projeto acadêmico.

**Resultado:** sugestão de aplicação web com API REST, banco de dados e um recurso de IA (cadastro assistido por foto), mais lista de elementos acadêmicos (requisitos, modelagem, testes, avaliação da IA, ética).

**Correções do autor:** o escopo foi redefinido pelo autor para uma **micro API CRUD** feita com apoio de LLM, com especificação, testes, repositório público, README, CI, tag e release. O recurso de IA no produto ficou como opcional pós-MVP.

**Avaliação:** 🔧 Ajuste. A sugestão inicial era maior que o escopo exigido e foi reduzida.

---

### Interação 02: Plano de execução da micro API

| | |
|---|---|
| **Data** | 2026-10-06 |
| **Fase** | Planejamento |
| **Objetivo** | Obter stack, estrutura de repositório, plano de commits e checklist de entrega |
| **Commit relacionado** | — |

**Prompt (resumo):**
> A ideia é criar uma micro API CRUD, feita com apoio de LLMs, com especificação, testes e código funcionando. Enviar para o GitHub em repositório público, com histórico de commits consistente, README completo, dependências e testes executáveis, tag e release final e testes automatizados.

**Resultado:** stack (FastAPI, SQLModel/SQLAlchemy, SQLite, pytest, ruff, GitHub Actions), estrutura de pastas, plano de 12 commits em Conventional Commits, fluxo de trabalho com LLM e checklist de entrega.

**Correções do autor:** [preencher, ou escrever "nenhuma"]

**Avaliação:** [preencher]

---

### Interação 03: Geração da especificação

| | |
|---|---|
| **Data** | 2026-10-06 |
| **Fase** | Especificação |
| **Objetivo** | Gerar `docs/ESPECIFICACAO.md` com requisitos, modelo de dados, contrato da API e critérios de aceite |
| **Commit relacionado** | `docs: adiciona especificação da API e critérios de aceite` |

**Prompt:**
> Pode gerar a especificação

*(O prompt foi curto porque o contexto já estava estabelecido nas interações 01 e 02: recurso `Item`, endpoints, campos e stack.)*

**Resultado:** documento com 10 requisitos funcionais, 10 não funcionais, modelo de dados com diagrama ER, contrato da API, 10 regras de negócio, 41 critérios de aceite (CA01–CA41) no formato Dado/Quando/Então, matriz de rastreabilidade, estratégia de testes, definição de pronto, marcos e riscos.

**Decisões tomadas pelo LLM e validadas pelo autor:**

- Exclusão física, não lógica
- Paginação padrão de 20 itens, máximo de 100
- Formato de temporada: `AAAA`, `AAAA/AA` ou `AAAA/AAAA`
- Endpoint de IA por foto fora do MVP

**Correções do autor:** nenhuma solicitada; o autor avaliou a especificação como aderente.

**Avaliação:** ✅ Acerto

**Observação para revisão do autor:** a especificação traz uma data de versão no histórico do documento. Conferir se corresponde à data real de criação.

---

### Interação 04: Roteiro para não programador e estimativa de esforço

| | |
|---|---|
| **Data** | 2026-10-06 |
| **Fase** | Preparação |
| **Objetivo** | Obter o passo a passo para executar o desenvolvimento no próprio computador; estimar o esforço restante |
| **Commit relacionado** | — |

**Prompt (resumo):**
> A especificação é aderente. Porém, eu não sou programador. Gostaria das etapas que devo executar em meu computador para evoluir com o desenvolvimento da solução.

Em seguida, o autor perguntou quantas horas seriam necessárias para finalizar o MVP.

**Resultado:** roteiro em fases (instalação de Python, Git e VS Code; criação do repositório; ambiente virtual; ciclo de desenvolvimento; fechamento com CI, README e release), com modelos de prompt e comandos para PowerShell. Estimativa de esforço restante de **8 a 12 horas**, distribuídas em 3 a 4 sessões.

**Correções do autor:** o autor decidiu **não** fazer os itens opcionais (Docker e endpoint de IA) nesta versão.

**Tempo real gasto:** [preencher, para comparar com a estimativa de 8 a 12 h]

**Avaliação:** [preencher]

---

### Interação 05: Ambiente, dependências e configuração do ruff/pytest

| | |
|---|---|
| **Data** | 2026-10-06 |
| **Fase** | Fase 2: Ambiente |
| **Objetivo** | Obter `requirements.txt` com versões fixas, `pyproject.toml` e o esqueleto de pastas |
| **Commit relacionado** | `chore: configura ambiente, dependências e ruff` |

**Prompt (modelo fornecido ao autor):**

```text
Contexto: estou desenvolvendo uma micro API REST de catálogo de artigos de
futebol (FastAPI + SQLModel + SQLite), com pytest, pytest-cov e ruff.
Não sou programador, então:
- entregue cada arquivo COMPLETO, com o caminho no topo;
- não omita trechos com "...";
- dê os comandos exatos para Windows PowerShell.

Estou na Fase 2 (ambiente). Preciso de:
1. A lista de pacotes a instalar (sem versões) e o comando pip install.
2. Como gerar o requirements.txt com versões fixas a partir do que for
   instalado (pip freeze), cuidando da codificação do arquivo no PowerShell.
3. Um pyproject.toml com a configuração do ruff (lint e format) e do pytest
   (pasta tests, pythonpath na raiz, cobertura do pacote app).
4. Os comandos para criar o esqueleto de pastas e arquivos vazios:
   app/ (main.py, models.py, schemas.py, database.py, routes/itens.py)
   e tests/ (test_itens_crud.py, test_filtros.py, test_validacoes.py,
   test_health.py).
5. Os comandos para verificar que tudo foi instalado corretamente.

Não implemente a API ainda.
```

**Resultado:** comando de instalação dos pacotes, geração do `requirements.txt` via `pip freeze` com `Out-File -Encoding utf8`, `pyproject.toml` com configuração de ruff e pytest, comandos de criação do esqueleto e de verificação.

**Decisão de processo relevante:** as versões **não** foram digitadas pelo LLM. O `requirements.txt` foi gerado com `pip freeze`, para evitar versões desatualizadas ou inexistentes (risco típico de alucinação em LLMs).

**Dúvida posterior do autor:** como criar o `pyproject.toml` na raiz do projeto. O LLM detalhou o passo a passo pelo VS Code e pelo terminal e listou erros comuns.

**Correções do autor:** o `line-length` do ruff estava em 88 no projeto, e a especificação previa 100. O autor corrigiu manualmente (ver Interação 09 e ocorrência O2).

**Avaliação:** 🔧 Ajuste

---

### Interação 06: Marco M2, testes de criação e consulta (CA01–CA12)

| | |
|---|---|
| **Data** | 2026-10-06 |
| **Fase** | Fase 3, ciclo TDD, passo 1 |
| **Objetivo** | Gerar `tests/conftest.py`, `tests/test_itens_crud.py` e `tests/test_validacoes.py` para CA01–CA12 |
| **Commit relacionado** | `test: adiciona testes de criação e consulta de item` |

**Prompt (enviado ao chat, com `ESPECIFICACAO.md` anexada; o mesmo texto foi colado também no agente do VS Code):**

```text
Contexto: estou desenvolvendo uma micro API REST de catálogo de artigos de
futebol (FastAPI + SQLModel + SQLite), com pytest, pytest-cov e ruff.
Já tenho o esqueleto de pastas criado (app/ e tests/, arquivos vazios) e o
pyproject.toml configurado. Não sou programador, então:
- entregue cada arquivo COMPLETO, com o caminho no topo;
- não omita trechos com "...";
- dê os comandos exatos para Windows PowerShell;
- explique em linguagem simples o que cada arquivo faz.

[ESPECIFICACAO.md anexada]

Tarefa (Marco M2, abordagem TDD): escreva APENAS OS TESTES, sem implementar
a API, cobrindo os critérios de aceite CA01 a CA12.

Requisitos:
1. Crie tests/conftest.py com fixtures que:
   - usem um banco SQLite em memória, isolado por teste;
   - sobrescrevam a dependência de sessão do app (dependency_overrides);
   - exponham um "client" (TestClient) e uma função auxiliar para criar itens.
2. Coloque os testes de CA01 a CA12 em tests/test_itens_crud.py e
   tests/test_validacoes.py, conforme a matriz de rastreabilidade.
3. Nomeie cada teste com o ID do critério (ex.: test_ca01_cria_item_completo).
4. Diga quais nomes e caminhos de módulos o código deverá ter
   (ex.: app.main:app, app.database:get_session) para que eu os informe
   na etapa de implementação.
```

**Resultado:**

- **Agente do VS Code:** criou arquivos de teste por conta própria, mas **não conseguiu executar `pytest` nem `ruff`** (execução de comandos negada). Reportou apenas que o editor não apontou erros, o que significa ausência de erro de sintaxe, não prova de cobertura dos critérios.
- **Chat:** entregou 3 arquivos (`conftest.py`, `test_itens_crud.py`, `test_validacoes.py`) com **26 testes**, validados contra uma implementação de referência (26 passando, `ruff` aprovado).

**Correções do autor:** os tamanhos em bytes dos arquivos gerados pelo agente eram diferentes dos entregues pelo chat. O autor **substituiu os arquivos do agente pelos validados no chat**. O primeiro `pytest` falhou com `ImportError: cannot import name 'get_session'`, que era o resultado esperado antes da implementação.

**Avaliação:** 🔧 Ajuste (versão do agente descartada; versão validada adotada)

---

### Interação 07: Marco M2, implementação de POST /itens e GET /itens/{id}

| | |
|---|---|
| **Data** | 2026-10-06 |
| **Fase** | Fase 3, ciclo TDD, passo 5 |
| **Objetivo** | Implementar `app/database.py`, `models.py`, `schemas.py`, `routes/itens.py` e `main.py` para os testes passarem |
| **Commit relacionado** | `feat: implementa POST /itens e GET /itens/{id}` |

**Prompt (enviado ao agente do VS Code):**

```text
Os testes do Marco M2 estão em tests/ (conftest.py, test_itens_crud.py,
test_validacoes.py) e falham, como esperado. Leia esses arquivos e a
docs/ESPECIFICACAO.md (seções 6, 7 e 8).

Implemente app/database.py, app/models.py, app/schemas.py,
app/routes/itens.py e app/main.py para os testes passarem, SEM alterar os
testes. Endpoints deste marco: apenas POST /itens e GET /itens/{id}.

Requisitos técnicos:
1. app.main:app é a aplicação FastAPI; app.database:get_session entrega a
   sessão do banco (os testes a substituem). app.models tem a tabela Item
   (SQLModel, table=True).
2. id, criado_em e atualizado_em enviados pelo cliente devem ser aceitos e
   IGNORADOS (CA08), mas campos desconhecidos devem dar 422 (CA09).
3. Use datas com fuso horário (UTC). Datas sem fuso causam erro no SQLModel.
4. Use Annotated[Session, Depends(get_session)], senão o ruff reprova (B008).
5. A criação das tabelas do banco real fica no startup (lifespan) do app;
   os testes não ativam o startup.
6. foto_url deve voltar exatamente como foi enviado (texto simples).
7. Remova espaços nas pontas dos textos antes de validar e salvar.

Você NÃO consegue rodar comandos aqui. Ao terminar, me diga os comandos
para eu rodar: pytest, ruff check . e ruff format .
```

**Resultado:** na primeira execução no computador do autor, **26 testes passaram**, com **87% de cobertura** (Python 3.14.8).

**Rodadas de correção necessárias:** nenhuma relatada.

**Efeito dos cuidados incluídos no prompt:** os pontos 2 a 4 (campos ignorados, datas com fuso, `Annotated`) vieram de problemas encontrados na validação com a implementação de referência (ver ocorrência O1). O código do agente passou sem erros de data.

**Avaliação:** ✅ Acerto

---

### Interação 08: Marco M3, testes de listagem, paginação e filtros (CA13–CA24)

| | |
|---|---|
| **Data** | 2026-10-07 |
| **Fase** | Fase 3, ciclo TDD, passo 1 |
| **Objetivo** | Gerar `tests/test_filtros.py` |
| **Commit relacionado** | `test: adiciona testes de listagem, paginação e filtros` |

**Solicitação (resumo):**
> Pode enviar o próximo.

**Resultado:** arquivo com **22 testes** (CA13 a CA24, mais um teste extra para o filtro por `versao`, previsto no RF04 mas sem critério de aceite). Validado contra implementação de referência: 48 testes no total passando, em 3 execuções seguidas.

**Correções do autor:** nenhuma no conteúdo. Ao executar, 22 testes falharam com `405`, como esperado antes da implementação.

**Avaliação:** ✅ Acerto

---

### Interação 09: Marco M3, implementação de GET /itens com filtros e paginação

| | |
|---|---|
| **Data** | 2026-10-07 |
| **Fase** | Fase 3, ciclo TDD, passo 5 |
| **Objetivo** | Implementar a listagem em `app/routes/itens.py` e `app/schemas.py` |
| **Commit relacionado** | `feat: implementa listagem com filtros e paginação` |

**Prompt (enviado ao agente do VS Code):**

```text
Os testes do Marco M3 estão em tests/test_filtros.py e falham, como esperado
(os 26 testes do M2 continuam passando). Leia esse arquivo e a
docs/ESPECIFICACAO.md (seções 7.2 e 8).

Implemente GET /itens em app/routes/itens.py (e o que mais for necessário
em app/schemas.py) para os testes passarem, SEM alterar nenhum teste e
SEM quebrar os testes do M2. Não implemente PUT, PATCH nem DELETE ainda.

Requisitos:
1. Resposta: {"itens": [...], "total": N, "pagina": P, "tamanho": T}.
2. Parâmetros: tipo, versao, temporada (igualdade exata), clube_selecao e
   fabricante (contém, sem diferenciar maiúsculas de minúsculas), pagina
   (inteiro >= 1, padrão 1) e tamanho (inteiro de 1 a 100, padrão 20).
3. Valores inválidos nos parâmetros devem dar 422 (ex.: tipo=invalido).
4. Filtros combinados usam E lógico. "total" conta apenas os itens que
   passam pelos filtros, não o total geral.
5. Ordenação: criado_em decrescente, desempate por id decrescente.
6. Use Annotated[Session, Depends(get_session)] (regra B008 do ruff).

Você NÃO consegue rodar comandos aqui. Ao terminar, me diga os comandos
para eu rodar: pytest, ruff check . e ruff format .
```

**Resultado:** **48 testes passaram** na primeira execução, com **89% de cobertura** e 100% em `routes/itens.py`. O teste manual no Swagger e com `curl` confirmou a listagem (4 itens, `total: 4`, ordem do mais recente para o mais antigo).

**Rodadas de correção necessárias:** nenhuma no código. Houve ajustes de configuração e de processo, registrados nas ocorrências O2, O3 e O4.

**Limitação observada:** o filtro de texto ignora maiúsculas, mas **não ignora acentos**. Com os itens cadastrados como "São Paulo", "sao paulo" e "são paulo", a busca por `sao` encontra só um deles. Está coerente com a especificação e foi registrado como trabalho futuro.

**Avaliação:** ✅ Acerto no código; 🔧 Ajustes de configuração e processo

---

### Interação 10: Marco M4, testes de atualização e exclusão (CA25–CA37)

| | |
|---|---|
| **Data** | 2026-10-07 |
| **Fase** | Fase 3, ciclo TDD, passo 1 |
| **Objetivo** | Atualizar `tests/test_itens_crud.py` e `tests/test_validacoes.py` com os testes de PUT, PATCH e DELETE |
| **Commit relacionado** | `test: adiciona testes de atualização e exclusão de item` |

**Solicitação (resumo):**
> Commit feito. Pode enviar o próximo.

**Resultado:** 19 testes novos (CA25 a CA37), totalizando 67. Validados contra implementação de referência (67 passando em 3 execuções seguidas) e por **teste de mutação** com 3 defeitos propositais, todos detectados (ver seção 2.1).

**Decisões de projeto nos testes:** em cada erro `422` o item é consultado depois para provar que **não foi alterado**; comparações de data toleram ausência de fuso; um `sleep` curto no CA31 evita falha por resolução do relógio.

**Correções do autor:** nenhuma no conteúdo. Ao executar antes da implementação, 19 testes falharam e 48 passaram, como esperado.

**Avaliação:** ✅ Acerto

---

### Interação 11: Marco M4, implementação de PUT, PATCH e DELETE

| | |
|---|---|
| **Data** | 2026-10-07 |
| **Fase** | Fase 3, ciclo TDD, passo 5 |
| **Objetivo** | Implementar PUT, PATCH e DELETE |
| **Commit relacionado** | `feat: implementa PUT, PATCH e DELETE de itens` |

**Prompt (enviado ao agente do VS Code):**

```text
Os testes do Marco M4 estão em tests/test_itens_crud.py e
tests/test_validacoes.py e falham, como esperado (os 48 testes dos marcos
M2 e M3 continuam passando). Leia esses arquivos e a docs/ESPECIFICACAO.md
(seções 7 e 8, regras RN01 a RN10).

Implemente PUT /itens/{id}, PATCH /itens/{id} e DELETE /itens/{id} em
app/routes/itens.py (e o que mais for necessário em app/schemas.py) para os
testes passarem, SEM alterar nenhum teste e SEM quebrar os existentes.

Requisitos:
1. PUT exige o objeto completo (tipo e clube_selecao obrigatórios). Campos
   opcionais omitidos voltam para null (RN06).
2. PATCH altera só os campos enviados. Enviar null limpa um campo opcional,
   mas tipo e clube_selecao não podem ser null (422) (RN07).
3. PUT e PATCH validam como o POST: mesmos formatos, enums, tamanhos e
   remoção de espaços nas pontas (RN02). Campos desconhecidos dão 422.
4. PUT e PATCH renovam atualizado_em (com fuso UTC) e NUNCA mudam id nem
   criado_em (RN05).
5. Item inexistente em PUT, PATCH ou DELETE: 404 com
   {"detail": "Item não encontrado"}.
6. DELETE retorna 204 sem corpo e é exclusão física (RN09).
7. Se a validação falhar (422), o item no banco não pode ser alterado.
8. Use Annotated[Session, Depends(get_session)] (regra B008 do ruff).

Você NÃO consegue rodar comandos aqui. Ao terminar, me diga os comandos
para eu rodar: pytest, ruff check . e ruff format .
```

**Resultado:** o **teste manual no Swagger** (PUT, PATCH, DELETE, erros 404 e 422) foi concluído com sucesso pelo autor. No CI, após a correção do commit esquecido (ocorrência O5), os 70 testes passaram.

**Rodadas de correção necessárias:** [preencher: número de rodadas no agente, se houve]

**Avaliação:** ✅ Acerto no código; ❌ Erro de processo no commit (ocorrência O5)

---

### Interação 12: Marco M5, testes do health check e da documentação (CA38, CA39)

| | |
|---|---|
| **Data** | 2026-10-07 |
| **Fase** | Fase 3, ciclo TDD, passo 1 |
| **Objetivo** | Gerar `tests/test_health.py` |
| **Commit relacionado** | `test: adiciona testes do health check e da documentação` |

**Solicitação (resumo):**
> Vamos para o próximo, porém não farei os opcionais nesse momento.

**Resultado:** 3 testes novos (`/health`, `/docs` e `/openapi.json`), totalizando 70. Na validação, **1 dos 3 já passava sem implementação**, porque o FastAPI entrega `/docs` automaticamente. Isso foi antecipado ao autor para evitar estranhamento.

**Avaliação:** ✅ Acerto

---

### Interação 13: Marco M5, implementação do GET /health

| | |
|---|---|
| **Data** | 2026-10-07 |
| **Fase** | Fase 3, ciclo TDD, passo 5 |
| **Objetivo** | Implementar `GET /health` em `app/main.py` |
| **Commit relacionado** | `feat: adiciona endpoint GET /health` |

**Prompt (enviado ao agente do VS Code):**

```text
Os testes de tests/test_health.py estão escritos e 2 deles falham, como
esperado (os 67 testes anteriores passam). Leia o arquivo e a
docs/ESPECIFICACAO.md (RF09, seção 7).

Implemente GET /health em app/main.py, retornando {"status": "ok"} com
status 200. Não deve acessar o banco de dados. Não altere nenhum teste e
não quebre os existentes.

Você NÃO consegue rodar comandos aqui. Ao terminar, me diga os comandos
para eu rodar: pytest, ruff check . e ruff format .
```

**Resultado:** [preencher: confirmar que os 70 testes passaram localmente e o teste manual em `/health`]

**Rodadas de correção necessárias:** [preencher]

**Avaliação:** [preencher]

---

### Interação 14: Marco M5, pipeline de integração contínua (CI)

| | |
|---|---|
| **Data** | 2026-10-07 |
| **Fase** | Integração contínua |
| **Objetivo** | Criar `.github/workflows/ci.yml` com lint, verificação de formatação e testes com cobertura mínima de 80% |
| **Commit relacionado** | `ci: adiciona pipeline com lint e testes` |

**Verificação feita pelo LLM antes de gerar o arquivo:** em vez de usar versões de memória, o LLM **consultou a página oficial do GitHub** (`actions/setup-python`) e confirmou que as versões atuais das ações eram `actions/checkout@v7` e `actions/setup-python@v7`. Também validou o YAML e simulou os passos do pipeline em um ambiente limpo, instalado só pelo `requirements.txt` (70 testes, 97% de cobertura).

**Resultado:**

- **1ª execução (vermelha):** falharam 19 testes, todos do M4, com `405 Method Not Allowed` e cobertura de 89,18%. Os passos de instalação do Python, instalação das dependências, `ruff check` e `ruff format --check` passaram. A causa foi o commit da implementação de PUT, PATCH e DELETE ter ficado de fora (ocorrência O5).
- **2ª execução (verde):** após o commit e o `push` da implementação, o CI passou.

**Pontos que não precisaram de correção:** Python 3.14 funcionou no GitHub Actions, e as ações na versão 7 funcionaram.

**Rodadas de correção necessárias no `ci.yml`:** nenhuma. A falha inicial foi de processo, não de configuração.

**Avaliação:** ✅ Acerto no arquivo; o CI cumpriu seu papel ao revelar o commit esquecido

---

### Interação 15: Marco M6, README, CHANGELOG e release v1.0.0

| | |
|---|---|
| **Data** | [preencher] |
| **Fase** | Fechamento |
| **Objetivo** | README completo com badge do CI, `CHANGELOG.md`, tag `v1.0.0` e GitHub Release |
| **Commit relacionado** | [preencher] |

*(Pendente. Registrar prompt, resultado e correções.)*

---

## 4. Ocorrências relevantes

| ID | Marco | Ocorrência | Causa | Resolução | Classe |
|---|---|---|---|---|---|
| O1 | M2 | Na validação dos testes, a primeira implementação de referência usou datas sem fuso horário e falhou ao gravar no banco | A versão instalada do SQLModel (0.0.48) exige datas com fuso. O padrão antigo, comum em exemplos e na memória do LLM, está desatualizado | Datas passaram a usar UTC. O cuidado foi **incluído nos prompts** seguintes ao agente | 👻 Informação desatualizada |
| O2 | M3 | `ruff check` apontou `E501` (linha com 94 caracteres, limite de 88) em `tests/test_filtros.py` | O `pyproject.toml` do projeto tinha `line-length` 88, enquanto a especificação e a validação dos testes usavam 100 | O autor alterou o valor para 100 e rodou `ruff format .`. As mudanças em outros arquivos (como `database.py`) foram só de formatação | 🔧 Ajuste |
| O3 | M3 | O arquivo de banco local `catalogo.db` estava versionado no GitHub | O roteiro sugeria `git add .`, e o `.gitignore` padrão de Python não ignora arquivos `.db` (causa provável) | `git rm --cached catalogo.db` e inclusão de `*.db` no `.gitignore`. A partir daí, `git add` por nome de arquivo. Versões antigas do banco permanecem no histórico (sem dados sensíveis) | ❌ Erro do roteiro do LLM |
| O4 | M3 | O autor relatou que o `GET /itens` "funcionava apenas para id" no Swagger | Causa provável: servidor antigo ainda em execução ou página em cache. Não foi comprovada | Reinício do servidor. A listagem respondeu `200` com os 4 itens | 🔧 Ajuste |
| O5 | M4 | CI vermelho com 19 testes falhando (`405 Method Not Allowed`) | `app/routes/itens.py` e `app/schemas.py` ficaram sem commit: o GitHub tinha os testes do M4, mas não a implementação. O código local estava correto | Commit e `push` dos dois arquivos. CI ficou verde | ❌ Erro de processo (esquecimento de commit) |
| O6 | M2 | O agente do VS Code não conseguiu executar `pytest` nem `ruff` | A execução de comandos foi negada no ambiente do agente | O autor executou os comandos manualmente no terminal | 🔧 Ajuste |

**Observação sobre O5:** a mensagem recebida como diagnóstico automático (de origem não identificada) afirmava que os endpoints não estavam implementados ou registrados. Isso estava correto para o código **no repositório**, mas não indicava a causa real (commit ausente). A conferência com `git status` foi o que revelou o motivo.

## 5. Modelo de prompt para correção de erros

Usado sempre que `pytest` ou `ruff` apontam falhas:

```text
Rodei `pytest` e deu o erro abaixo. Explique a causa em linguagem simples
e me entregue os arquivos corrigidos por completo, sem alterar os testes
(a menos que o teste esteja errado em relação à especificação; se for o
caso, explique).

[erro completo colado aqui]
```

## 6. Modelo para novas entradas

```markdown
### Interação NN: Título

| | |
|---|---|
| **Data** | AAAA-MM-DD |
| **Fase** | |
| **Objetivo** | |
| **Commit relacionado** | |

**Prompt:**

**Resultado:**

**Correções do autor:**

**Avaliação:** ✅ / 🔧 / ❌ / 👻
```

---

## 7. Resumo quantitativo

| Marco | Testes ao final | Cobertura | Rodadas de correção do código | Ocorrências |
|---|---|---|---|---|
| Planejamento e especificação | — | — | — | — |
| Ambiente (Fase 2) | 0 | — | — | O2 (origem) |
| M2: criar e consultar | 26 | 87% | 0 relatadas | O1, O6 |
| M3: listagem e filtros | 48 | 89% | 0 relatadas | O2, O3, O4 |
| M4: atualização e exclusão | 67 | [preencher] | [preencher] | O5 |
| M5: health e CI | 70 | 89,18% na 1ª execução do CI (com 19 falhas); [preencher] na execução verde | [preencher] | O5 |
| M6: documentação e release | — | — | — | — |

| Indicador | Valor |
|---|---|
| Testes automatizados no final | 70 |
| Critérios de aceite cobertos | CA01 a CA39 por testes automatizados; CA40 e CA41 verificados pelo CI |
| Tempo estimado pelo LLM | 8 a 12 horas |
| Tempo real gasto | [preencher] |

## 8. Reflexão final

*(O autor deve revisar, reescrever com suas palavras e completar ao concluir o projeto. Os pontos abaixo são fatos já observados e servem de rascunho.)*

### 8.1 Onde o LLM ajudou mais

- Especificação com critérios de aceite rastreáveis, que viraram testes diretamente.
- Testes escritos antes do código e validados com implementação de referência e mutação, o que levou os marcos M2 a M4 a passarem na primeira execução com o código do agente.
- Roteiro passo a passo para um autor não programador.
- Verificação de versões atuais (ações do GitHub) em fonte oficial, em vez de depender da memória.

**Complemento do autor:** [preencher]

### 8.2 Onde o LLM errou ou exigiu correção

- Roteiro com `git add .` que levou o banco local ao repositório (O3).
- Configuração de `line-length` divergente entre a especificação e o projeto (O2).
- Agente do VS Code sem capacidade de executar comandos e com testes próprios diferentes dos validados (O6).

**Complemento do autor:** [preencher]

### 8.3 Alucinações e informações desatualizadas identificadas

- Uso de datas sem fuso horário, padrão antigo incompatível com a versão instalada do SQLModel (O1).

**Complemento do autor:** [preencher]

### 8.4 Como a especificação e os testes reduziram riscos

- Critérios de aceite numerados (CA01–CA41) permitiram verificar objetivamente cada marco.
- O CI detectou que o código no repositório não correspondia ao código local (O5), problema que o `pytest` local não mostraria.
- Os testes de erro confirmam que o item **não é alterado** quando a validação falha.

**Complemento do autor:** [preencher]

### 8.5 Limitações da abordagem para um autor não programador

- Dependência de comandos copiados do LLM, com risco de esquecer etapas do roteiro (O5).
- Dificuldade de distinguir problemas de código, de configuração e de ambiente (O2, O4).

**Complemento do autor:** [preencher]

### 8.6 Limitações do produto e trabalhos futuros

- Filtro de texto sem tratamento de acentos e sem padronização de nomes de clubes.
- Sem autenticação, upload de fotos nem Docker (opcionais não implementados).
- Cadastro assistido por IA (envio de foto e sugestão de campos) previsto como evolução, com avaliação de acurácia por campo.

### 8.7 Lições aprendidas e boas práticas

- Adicionar arquivos ao Git por nome, e conferir `git status` antes de cada commit.
- Rodar testes e `ruff` localmente **e** conferir o CI após cada `push`.
- Pedir ao LLM para validar versões e comandos em fontes oficiais.
- [preencher]

### 8.8 Considerações éticas

- Responsabilidade do autor pela revisão e validação de todo código gerado.
- Transparência: o uso de LLM é declarado neste documento e no README.
- Privacidade: nenhum dado sensível foi enviado ao LLM. As imagens usadas nos testes manuais são URLs públicas.
- [preencher outros pontos]
