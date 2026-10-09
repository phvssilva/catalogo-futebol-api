# Changelog

Todas as mudanças relevantes deste projeto são registradas neste arquivo.

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o projeto adota o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-10-07

Primeira versão do MVP: micro API REST para catalogar uma coleção de artigos de futebol.

### Adicionado

- Recurso `Item` com CRUD completo:
  - `POST /itens` para criar
  - `GET /itens/{id}` para consultar
  - `PUT /itens/{id}` para substituir todos os campos
  - `PATCH /itens/{id}` para atualizar parcialmente
  - `DELETE /itens/{id}` para excluir (exclusão física)
- `GET /itens` com paginação (`pagina`, `tamanho`) e filtros por `tipo`, `clube_selecao`, `temporada`, `fabricante` e `versao`, ordenado do mais recente para o mais antigo
- Validação de dados: campos obrigatórios, valores permitidos para `tipo`, `versao` e `condicao`, formato de `temporada`, URL de `foto_url`, tamanhos máximos, remoção de espaços nas pontas e rejeição de campos desconhecidos
- Geração automática de `id`, `criado_em` e `atualizado_em` (UTC)
- `GET /health` para verificação de saúde
- Documentação interativa (Swagger UI em `/docs` e OpenAPI em `/openapi.json`)
- 70 testes automatizados com pytest, banco SQLite em memória isolado por teste e cobertura mínima de 80%
- Integração contínua com GitHub Actions (Ruff e pytest)
- Especificação com requisitos, regras de negócio e 41 critérios de aceite (`docs/ESPECIFICACAO.md`)
- Registro do uso de LLM no desenvolvimento (`docs/uso-de-llm.md`)
- README com instalação, execução, exemplos e estrutura do projeto

### Alterado

- Banco local `catalogo.db` removido do versionamento e arquivos `*.db` incluídos no `.gitignore`
- Limite de linha do Ruff ajustado para 100 caracteres

### Limitações conhecidas

- Filtros de texto não ignoram acentos
- Sem autenticação
- Sem Dockerfile e sem cadastro assistido por IA (previstos como evolução)

[1.0.0]: https://github.com/phvssilva/catalogo-futebol-api/releases/tag/v1.0.0

