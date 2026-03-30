# Prompts Utilizados — Engenharia Reversa

Este documento descreve os prompts que foram (ou poderiam ter sido) utilizados para gerar cada camada de artefatos do projeto KiroSonar, desde a documentação fundacional até o código-fonte.

---

## Camada 1 — Fundação (Documentos-Base)

### 1.1 RFC de Arquitetura (`backend/docs/RFC-001-KiroSonar-MVP.md`)

```
Crie uma RFC (Request for Comments) para um projeto chamado KiroSonar.

O KiroSonar é uma CLI em Python que funciona como um "SonarQube tunado com IA". 
Ele analisa o git diff do desenvolvedor, envia o código para uma LLM avaliar com 
base nas regras da empresa, gera um relatório no estilo SonarQube (Bugs, Smells, 
Vulnerabilidades, Hotspots) e aplica refatoração automática com aprovação humana (s/n).

A RFC deve conter:
1. O Problema (fricção do SonarQube tradicional)
2. A Solução Proposta (fluxo da CLI)
3. Arquitetura e Fluxo High Level (input → descoberta → análise → output → auto-fix)
4. Stack Tecnológica (Python 3.11+, apenas Standard Library, pyproject.toml com console_scripts)
5. Padrões de Código (PEP 8, Type Hinting, Docstrings, SOLID)
6. Fora do Escopo (sem CI/CD, sem dashboard web)
7. Riscos e Mitigações (custo de tokens, alucinação da IA)
```

### 1.2 PRD — Product Requirements Document (`.kiro/PRD.md`)

```
Com base na RFC #RFC-001-KiroSonar-MVP.md, crie um PRD completo para o KiroSonar.

O PRD deve expandir a RFC com:
- Visão Geral e Problema detalhado
- Solução com os 4 passos (git diff → LLM → relatório → auto-fix)
- Personas (Desenvolvedor Fullstack, Tech Lead, Analista de Qualidade)
- Requisitos Funcionais detalhados:
  - RF-01: Análise via Git Diff com envio de diff (peso máximo) + arquivo completo (peso médio)
  - RF-02: Auto-Fix interativo com tags [START]/[END] e confirmação s/n
  - RF-03: Regras personalizáveis via regras_empresa.md com DEFAULT_RULES como fallback
- Requisitos Não-Funcionais (Python 3.11+, Standard Library only, UTF-8, KIROSONAR_MOCK=1)
- User Stories (US-01, US-02, US-03)
- Arquitetura de Módulos (cli, git_module, config, prompt_builder, ai_service, report, autofix)
- Fluxo Principal completo
- Critérios de Aceitação do MVP
- Fora do Escopo e Riscos
```

### 1.3 Padrão de Projeto (`.kiro/padrao-projeto.md`)

> Este arquivo foi fornecido pelo professor como diretriz organizacional. Não foi gerado por prompt, mas sim usado como input para os demais artefatos.

Conteúdo define: estrutura de repositório monorepo, nomenclatura, gitflow, commit semântico e tópicos do README.

### 1.4 Instructions do Agente (`.kiro/instructions.md`)

```
Crie um arquivo de instruções para o agente IA que vai auxiliar o time a construir 
o KiroSonar. O agente deve se comportar como um Engenheiro de Software Sênior 
especialista em Python e CLI.

Defina:
- Identidade e papel do agente
- Contexto do projeto KiroSonar (CLI, git diff, LLM, relatórios, auto-fix)
- Stack: Python 3.11+, apenas Standard Library, pytest para testes
- Política de idiomas:
  - Código (variáveis, funções, classes, docstrings): 100% Inglês
  - Comentários de código e prints: Português Brasil
  - Documentação (README, RFC, Tickets, Code Reviews): 100% Português Brasil
- Padrões: PEP 8, Type Hinting, Docstrings, SOLID, Clean Architecture
- Diretrizes de comportamento: ler /docs antes de implementar, modo plan, modularidade
- Fluxo de entrega (Definition of Done): código + testes + guideline de code review
- Estrutura do projeto (índice de diretórios)
```

---

## Camada 2 — Tickets de Implementação

### 2.1 TASK-01: CLI Base (`backend/docs/tickets/TASK-01-cli-base.md`)

```
Com base no #PRD.md e no #padrao-projeto.md, crie um ticket de desenvolvimento 
para a TASK-01: CLI Base, Entry Point e Configuração.

O ticket deve definir:
- Branch: feature/cli-base
- Módulos a criar: pyproject.toml, src/__init__.py, src/cli.py, src/config.py
- Escopo técnico detalhado para cada módulo:
  - pyproject.toml com console_scripts (kirosonar = "src.cli:main")
  - cli.py com fail-fast de versão Python >= 3.11, argparse com subcomando analyze 
    e flags --path e --rules
  - config.py com load_rules() e DEFAULT_RULES como fallback
- Contratos expostos (tabela com função, input, output)
- Contratos consumidos com mocks sugeridos (git_module, ai_service, report, autofix)
- Critérios de aceite (Definition of Done) como checklist
```

### 2.2 TASK-02: Módulo Git Diff (`backend/docs/tickets/TASK-02-git-diff.md`)

```
Com base no #PRD.md, crie um ticket de desenvolvimento para a TASK-02: Módulo Git Diff.

O ticket deve definir:
- Branch: feature/git-diff
- Módulo a criar: src/git_module.py
- Escopo técnico:
  - get_changed_files() usando subprocess.run(["git", "diff", "--name-only"]) 
    com capture_output=True e text=True
  - Verificação de returncode para detectar se não é repo Git → sys.exit(1)
  - Filtro de linhas vazias do output
  - read_file_content(file_path) com encoding UTF-8
- Contratos expostos e consumidos
- Critérios de aceite
```

### 2.3 TASK-03: Serviço de IA (`backend/docs/tickets/TASK-03-ai-service.md`)

```
Com base no #PRD.md, crie um ticket de desenvolvimento para a TASK-03: 
Módulo Serviço de IA (LLM via Subprocesso).

O ticket deve definir:
- Branch: feature/ai-service
- Módulos a criar: src/ai_service.py e src/prompt_builder.py
- Escopo técnico:
  - ai_service.py: call_llm(prompt) usando subprocess.run(["kiro-cli", "chat", "--message", prompt])
  - Flag KIROSONAR_MOCK=1 para retornar MOCK_RESPONSE sem chamar subprocesso real
  - MOCK_RESPONSE com as 5 seções (Bugs, Vulnerabilidades, Code Smells, Hotspots, 
    Código Refatorado) e tags [START]/[END]
  - prompt_builder.py: build_prompt(code, rules, file_path) montando prompt com 
    regras + código + template fixo de resposta
- Template que o prompt deve forçar na resposta da LLM (5 seções + [START]/[END])
- Contratos e critérios de aceite
```

### 2.4 TASK-04: Relatório (`backend/docs/tickets/TASK-04-report.md`)

```
Com base no #PRD.md, crie um ticket de desenvolvimento para a TASK-04: 
Módulo de Geração de Relatório.

O ticket deve definir:
- Branch: feature/report
- Módulo a criar: src/report.py
- Escopo técnico:
  - save_report(content, file_path) salvando .md em relatorios/ com encoding UTF-8
  - generate_report_name(file_path) com nome do arquivo + timestamp YYYYMMDD_HHMMSS
  - Criação automática da pasta relatorios/ via os.makedirs
  - Substituição de / por _ no nome do relatório
- Mock MOCK_CONTENT para desenvolvimento independente
- Contratos e critérios de aceite
```

### 2.5 TASK-05: Auto-Fix (`backend/docs/tickets/TASK-05-autofix.md`)

```
Com base no #PRD.md, crie um ticket de desenvolvimento para a TASK-05: 
Módulo Auto-Fix (Parser + Aplicação).

O ticket deve definir:
- Branch: feature/autofix
- Módulo a criar: src/autofix.py
- Escopo técnico:
  - extract_refactored_code(ai_response) usando regex r'\[START\]\s*\n(.*?)\n\s*\[END\]' 
    com re.DOTALL, retornando str | None
  - apply_fix(ai_response, file_path) com preview de 20 linhas, prompt interativo 
    "Deseja aplicar o fix? (s/n)", sobrescrita apenas com s/S
- Mock MOCK_AI_RESPONSE para desenvolvimento independente
- Contratos e critérios de aceite
```

---

## Camada 3 — User Stories e Code Reviews

### 3.1 User Stories (`frontend/docs/user-stories/`)

```
Com base no #PRD.md, crie 3 User Stories detalhadas para o KiroSonar:

US-01: Análise automática dos arquivos alterados via Git Diff
- Formato: Como desenvolvedor... quero... para que...
- Contexto da filosofia "Clean as You Code"
- Critérios de aceite detalhados
- Módulos envolvidos (tabela)
- Fluxo em pseudocódigo
- Notas técnicas (git diff --name-only, KIROSONAR_MOCK=1)

US-02: Aplicação interativa de Auto-Fix sugerido pela IA
- Foco no diferencial competitivo vs SonarQube
- Aprovação humana obrigatória (s/n)
- Regex [START]/[END], preview 20 linhas
- Sem rollback no MVP (usar git checkout)

US-03: Personalização das regras de análise por projeto
- Persona: tech lead
- regras_empresa.md em linguagem natural (Markdown)
- DEFAULT_RULES como fallback
- Flag --rules para caminho alternativo
- Exemplo de regras_empresa.md
```

### 3.2 Code Reviews (`frontend/docs/code-review/`)

> Estes arquivos foram gerados automaticamente como parte do fluxo de entrega 
> definido no `.kiro/instructions.md` (Definition of Done: código + testes + guideline de code review).

```
Com base na implementação da TASK-01, gere um guideline de code review em 
docs/code-review/TASK-01-review.md seguindo o padrão do instructions.md:

- Checklist de Contrato (tabela com função, input esperado, output esperado, validado?)
- Pontos Críticos para o Revisor (linhas sensíveis, decisões de design, edge cases)
- Política de Idiomas (inglês no código, português nos prints/comentários)
- Comando de Teste (pytest tests/test_xxx.py -v)
```

```
Com base na implementação da TASK-02, gere um guideline de code review em 
docs/code-review/TASK-02-review.md seguindo o mesmo padrão:

- Checklist de Contrato para get_changed_files() e read_file_content()
- Pontos Críticos: subprocess.run params, returncode check, filtro de linhas vazias, 
  encoding UTF-8
- Critérios de Aceite como checklist
```

---

## Camada 4 — Specs do Kiro (Geradas via Kiro Specs)

### 4.1 Spec CLI Base (`.kiro/specs/cli-base/`)

```
Usando #TASK-01-cli-base.md crie um spec para implementar a task descrita. 
Siga tambem os documentos #PRD.md e #padrao-projeto.md
```

> Este prompt está registrado no próprio `prompts.md` original. O Kiro gerou 
> automaticamente os 3 arquivos: `requirements.md`, `design.md` e `tasks.md`.

### 4.2 Spec Git Diff Module (`.kiro/specs/git-diff-module/`)

```
Usando #TASK-02-git-diff.md crie um spec para implementar a task descrita. 
Siga tambem os documentos #PRD.md e #padrao-projeto.md
```

### 4.3 Spec AI Service (`.kiro/specs/ai-service/`)

```
Usando #TASK-03-ai-service.md crie um spec para implementar a task descrita. 
Siga tambem os documentos #PRD.md e #padrao-projeto.md
```

---

## Camada 5 — Código-Fonte (Gerado a partir das Specs)

> O código-fonte foi gerado pelo Kiro executando as tasks definidas nos specs. 
> Cada módulo foi implementado seguindo o design e os contratos definidos.

### 5.1 Implementação do Backend (`backend/src/`)

```
Execute as tasks do spec cli-base para implementar src/cli.py e src/config.py 
conforme o design definido.
```

```
Execute as tasks do spec git-diff-module para implementar src/git_module.py 
conforme o design definido.
```

```
Execute as tasks do spec ai-service para implementar src/ai_service.py e 
src/prompt_builder.py conforme o design definido.
```

> Para `src/report.py` e `src/autofix.py`, não há specs no `.kiro/specs/`, 
> indicando que foram implementados diretamente a partir dos tickets TASK-04 e TASK-05:

```
Implemente o módulo src/report.py conforme definido em #TASK-04-report.md. 
Siga os padrões do #PRD.md e #instructions.md.
```

```
Implemente o módulo src/autofix.py conforme definido em #TASK-05-autofix.md. 
Siga os padrões do #PRD.md e #instructions.md.
```

### 5.2 Implementação do Frontend (`frontend/src/`)

> O frontend replica parcialmente a estrutura do backend (cli.py, config.py, git_module.py) 
> e possui testes próprios. Provavelmente foi gerado com:

```
Com base na estrutura do backend e nos documentos #PRD.md e #padrao-projeto.md, 
crie a estrutura frontend do KiroSonar com os módulos: src/cli.py, src/config.py 
e src/git_module.py. Inclua testes em tests/.
```

---

## Camada 6 — README e Artefatos Finais

### 6.1 README.md

```
Conforme o padrao de projeto estabelecido pelo professor atualize o readme para o padrao
```

> Arquivo de referência utilizado como contexto: `backend/docs/padrao-projeto.md` 
> (agora em `.kiro/padrao-projeto.md`). O padrão exige: Nome do Projeto, Breve descrição, 
> Sumário de documentações, Tecnologias utilizadas, Instruções de instalação/uso, 
> Integrantes do grupo.

---

Preciso que você configure o Ruff como linter e formatter do projeto KiroSonar, seguindo estas instruções:
                                                                                                                                                                                                                                    
## 1. Instalação                                                                                                                                 

Adicione o ruff como dependência de desenvolvimento no `backend/pyproject.toml` usando o grupo `[project.optional-dependencies]` com a chave `dev`. Depois rode `pip install -e ".[dev]"` para instalar.                            

## 2. Configuração no pyproject.
Adicione a seção `[tool.ruff]` no `backend/pyproject.toml` com estas convenções:                                                                                                                                - Target: Python 3.11
- Line length: 99
- Regras habilitadas:
    - E (pycodestyle errors)
    - W (pycodestyle warnings)
    - F (pyflakes)
    - I (isort — ordenação de imports)
    - N (pep8-naming)

---

Configure um pre-commit hook do Git no projeto KiroSonar que rode o Ruff automaticamente antes de cada commit e bloqueie o commit se houver violações. Siga estas instruções:

## 1. Criar o hook

Crie o arquivo `scripts/pre-commit` (sem extensão) com o seguinte comportamento: 

- Rodar `ruff check backend/` nos arquivos Python do backend
- Se o ruff encontrar erros, exibir mensagem "❌ Lint falhou. Corrija os erros antes de commitar." e bloquear o commit (exit 1)
- Se passar, rodar `ruff format --check backend/`
- Se a formatação estiver errada, exibir mensagem "❌ Formatação incorreta. Rode 'ruff format backend/' antes de commitar." e bloquear o commit (exit 1)

- Se tudo passar, exibir "✅ Lint e formatação OK" e permitir o commit (exit 0)

## 2. Script de instalação do hook

Crie o arquivo `scripts/install-hooks.sh` que:
- Copia `scripts/pre-commit` para `.git/hooks/pre-commit` 
- Dá permissão de execução (`chmod +x`)
- Exibe mensagem de confirmação
