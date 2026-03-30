# Documento de Requisitos

## Introdução

Configuração do Ruff como linter e formatter oficial do projeto KiroSonar, acompanhado de um pre-commit hook do Git que bloqueia commits com violações de lint, formatação ou testes falhando. O objetivo é garantir qualidade de código consistente em todo o time, de forma automatizada e cross-platform (Linux, macOS, Windows/PowerShell).

## Glossário

- **Ruff**: Linter e formatter Python extremamente rápido, escrito em Rust. Substitui flake8, isort, pyupgrade e black em uma única ferramenta.
- **Pre-commit Hook**: Script executado automaticamente pelo Git antes de finalizar um commit. Se retornar exit code != 0, o commit é bloqueado.
- **Lint**: Análise estática de código para detectar erros, code smells e violações de estilo.
- **Format**: Formatação automática de código seguindo regras de estilo definidas.

---

## Requisitos

### Requisito 1: Ruff como Dependência de Desenvolvimento

**User Story:** Como desenvolvedor, quero que o Ruff esteja configurado como dependência do projeto, para que todos no time usem a mesma versão e configuração.

#### Critérios de Aceite

1. WHEN `pip install -e ".[dev]"` é executado no diretório `backend/`, THE sistema SHALL instalar o Ruff automaticamente.
2. WHEN o `pyproject.toml` é inspecionado, THE seção `[project.optional-dependencies]` SHALL conter a chave `dev` com `ruff` listado.

### Requisito 2: Configuração de Regras do Ruff

**User Story:** Como tech lead, quero que as regras de lint estejam centralizadas no `pyproject.toml`, para que todo o time siga as mesmas convenções sem configuração manual.

#### Critérios de Aceite

1. WHEN `ruff check backend/` é executado, THE Ruff SHALL usar target Python 3.11 e line-length 120.
2. WHEN o código viola regras E, W, F, I, N, UP, B, SIM ou D, THE Ruff SHALL reportar a violação.
3. WHEN um arquivo `__init__.py` não possui docstring de módulo, THE Ruff SHALL ignorar a regra D104.
4. WHEN um arquivo em `tests/` não possui docstring de módulo, THE Ruff SHALL ignorar a regra D100.
5. WHEN docstrings são avaliadas, THE Ruff SHALL usar a convenção Google.

### Requisito 3: Pre-commit Hook com Lint, Format e Testes

**User Story:** Como desenvolvedor, quero que o Git bloqueie meus commits automaticamente se houver problemas de lint, formatação ou testes falhando, para que código com defeito nunca entre no repositório.

#### Critérios de Aceite

1. WHEN `git commit` é executado, THE hook SHALL rodar `ruff check backend/` como primeira etapa.
2. WHEN o lint falha, THE hook SHALL exibir "❌ Lint falhou. Corrija os erros antes de commitar." e bloquear o commit (exit 1).
3. WHEN o lint passa, THE hook SHALL rodar `ruff format --check backend/` como segunda etapa.
4. WHEN a formatação falha, THE hook SHALL exibir "❌ Formatação incorreta. Rode 'ruff format backend/' antes de commitar." e bloquear o commit (exit 1).
5. WHEN a formatação passa, THE hook SHALL rodar `python -m pytest backend/tests/ -q` como terceira etapa.
6. WHEN os testes falham, THE hook SHALL exibir "❌ Testes falharam. Corrija os testes antes de commitar." e bloquear o commit (exit 1).
7. WHEN todas as etapas passam, THE hook SHALL exibir "✅ Lint, formatação e testes OK." e permitir o commit (exit 0).

### Requisito 4: Instalação Cross-Platform do Hook

**User Story:** Como desenvolvedor usando Windows (PowerShell), quero instalar o hook sem depender de bash ou sh, para que a configuração funcione em qualquer sistema operacional.

#### Critérios de Aceite

1. WHEN `python scripts/install_hooks.py` é executado, THE script SHALL copiar `scripts/pre-commit` para `.git/hooks/pre-commit`.
2. WHEN o hook é copiado, THE script SHALL dar permissão de execução ao arquivo.
3. WHEN a instalação é concluída, THE script SHALL exibir mensagem de confirmação.
4. WHEN o script é executado fora de um repositório Git, THE script SHALL exibir mensagem de erro e não falhar silenciosamente.

### Requisito 5: Código Existente em Conformidade

**User Story:** Como desenvolvedor, quero que todo o código existente do backend já esteja em conformidade com o Ruff, para que o hook não bloqueie commits legítimos.

#### Critérios de Aceite

1. WHEN `ruff check backend/` é executado no código existente, THE resultado SHALL ser zero violações.
2. WHEN `ruff format --check backend/` é executado no código existente, THE resultado SHALL ser zero diferenças.
3. WHEN `python -m pytest backend/tests/ -v` é executado após as correções de lint, THE resultado SHALL ser todos os 26 testes passando.
