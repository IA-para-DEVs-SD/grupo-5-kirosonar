# Design Técnico: ruff-precommit

## Visão Geral

Esta feature adiciona o Ruff como linter/formatter oficial do KiroSonar e um pre-commit hook do Git que garante qualidade de código antes de cada commit. A solução é 100% Python (cross-platform) e não depende de bash, sh ou qualquer ferramenta específica de sistema operacional.

Componentes:

- **Configuração do Ruff** no `backend/pyproject.toml`
- **Pre-commit hook** em `scripts/pre-commit` (Python puro)
- **Instalador do hook** em `scripts/install_hooks.py` (Python puro)

---

## Arquitetura

```
git commit
    │
    ▼
.git/hooks/pre-commit (cópia de scripts/pre-commit)
    │
    ├─ 1. ruff check backend/         → falhou? exit 1
    ├─ 2. ruff format --check backend/ → falhou? exit 1
    ├─ 3. python -m pytest backend/tests/ -q → falhou? exit 1
    └─ 4. tudo ok → exit 0 (commit prossegue)
```

---

## Configuração do Ruff (`backend/pyproject.toml`)

```toml
[project.optional-dependencies]
dev = ["ruff"]

[tool.ruff]
target-version = "py311"
line-length = 120

[tool.ruff.lint]
select = ["E", "W", "F", "I", "N", "UP", "B", "SIM", "D"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["D104"]
"tests/*" = ["D100"]
```

### Regras selecionadas

| Código | Plugin | O que faz |
|---|---|---|
| E | pycodestyle | Erros de estilo PEP 8 |
| W | pycodestyle | Warnings de estilo PEP 8 |
| F | pyflakes | Imports não usados, variáveis indefinidas |
| I | isort | Ordenação de imports |
| N | pep8-naming | Convenções de nomenclatura |
| UP | pyupgrade | Modernização de sintaxe Python |
| B | flake8-bugbear | Bugs comuns e anti-patterns |
| SIM | flake8-simplify | Simplificações de código |
| D | pydocstyle | Docstrings (convenção Google) |

---

## Pre-commit Hook (`scripts/pre-commit`)

- Shebang: `#!/usr/bin/env python3`
- Usa `subprocess.run` para executar cada etapa
- Usa `sys.executable` para o pytest (garante o Python do ambiente ativo — Conda)
- Retorna exit 1 na primeira falha (fail-fast)
- Mensagens em português com emojis para feedback visual

---

## Instalador (`scripts/install_hooks.py`)

- Usa `shutil.copy2` para copiar o hook
- Usa `os.chmod` com `stat.S_IEXEC` para dar permissão de execução
- Valida que está na raiz de um repositório Git (`.git/` existe)
- Valida que o arquivo fonte existe

---

## Restrições

- Apenas Standard Library Python (o instalador e o hook não dependem de pacotes externos)
- O Ruff é dependência de desenvolvimento, não de produção
- O hook é Python puro — funciona em Linux, macOS e Windows (PowerShell)
