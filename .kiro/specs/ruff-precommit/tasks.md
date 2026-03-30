# Plano de Implementação: ruff-precommit

## Visão Geral

Configuração do Ruff como linter/formatter e criação de pre-commit hook cross-platform com lint, formatação e testes unitários. Os arquivos `scripts/pre-commit` e `scripts/install_hooks.py` já existem com implementação parcial. As tasks abaixo cobrem a configuração completa e validação.

## Tasks

- [x] 1. Adicionar Ruff ao `backend/pyproject.toml`
  - Adicionar `[project.optional-dependencies]` com `dev = ["ruff"]`
  - Adicionar seção `[tool.ruff]` com `target-version = "py311"` e `line-length = 120`
  - Adicionar `[tool.ruff.lint]` com `select = ["E", "W", "F", "I", "N", "UP", "B", "SIM", "D"]`
  - Adicionar `[tool.ruff.lint.pydocstyle]` com `convention = "google"`
  - Adicionar `[tool.ruff.lint.per-file-ignores]` para `__init__.py` (D104) e `tests/*` (D100)
  - Rodar `pip install -e ".[dev]"` para instalar
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 2. Corrigir violações de lint no código existente
  - Rodar `ruff check backend/` e corrigir todas as violações
  - Rodar `ruff format backend/` para formatar o código
  - Garantir que `ruff check backend/` retorna zero violações
  - Garantir que `ruff format --check backend/` retorna zero diferenças
  - NÃO alterar lógica dos testes, apenas formatação e estilo
  - _Requirements: 5.1, 5.2_

- [x] 3. Criar/atualizar pre-commit hook em `scripts/pre-commit`
  - Shebang `#!/usr/bin/env python3`
  - Etapa 1: `ruff check backend/` → falhou? mensagem + exit 1
  - Etapa 2: `ruff format --check backend/` → falhou? mensagem + exit 1
  - Etapa 3: `python -m pytest backend/tests/ -q` → falhou? mensagem + exit 1
  - Etapa 4: tudo ok → mensagem de sucesso + exit 0
  - Usar `sys.executable` para o pytest
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_

- [x] 4. Criar/atualizar instalador em `scripts/install_hooks.py`
  - Copiar `scripts/pre-commit` para `.git/hooks/pre-commit`
  - Dar permissão de execução via `os.chmod`
  - Validar que `.git/` existe
  - Validar que `scripts/pre-commit` existe
  - Exibir mensagem de confirmação
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 5. Validar testes após correções de lint
  - Rodar `python -m pytest backend/tests/ -v`
  - Confirmar que todos os 26 testes passam
  - _Requirements: 5.3_

- [ ] 6. Atualizar README.md
  - Adicionar `python scripts/install_hooks.py` na seção "Configuração do Ambiente de Desenvolvimento"
  - Documentar que o hook roda lint, formatação e testes antes de cada commit
  - _Requirements: 4.3_
