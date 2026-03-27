# Requirements Document

## Introduction

O módulo `git_module.py` é a camada de infraestrutura do KiroSonar responsável por duas responsabilidades distintas: (1) detectar quais arquivos foram modificados no working tree via `git diff --name-only`, e (2) ler o conteúdo completo de um arquivo para envio à LLM. O módulo não possui dependências externas além da Standard Library do Python (`subprocess`, `sys`, `os`) e é consumido diretamente pelo `cli.py`.

## Glossary

- **Git_Module**: O módulo `backend/src/git_module.py` — camada de infraestrutura de integração com Git.
- **Working_Tree**: O estado atual dos arquivos no repositório Git local, incluindo modificações não comitadas.
- **Changed_Files**: Lista de caminhos relativos de arquivos com modificações detectadas pelo `git diff --name-only`.
- **Git_Repo**: Diretório que contém um repositório Git válido (possui `.git/`).
- **Subprocess**: Mecanismo da Standard Library Python para execução de processos externos.

## Requirements

### Requirement 1: Detecção de Arquivos Alterados

**User Story:** Como desenvolvedor, quero que o KiroSonar detecte automaticamente os arquivos que modifiquei, para que apenas o código relevante seja enviado para análise pela IA.

#### Acceptance Criteria

1. WHEN `get_changed_files()` é invocada dentro de um Git_Repo com arquivos modificados no Working_Tree, THE Git_Module SHALL executar `git diff --name-only` via Subprocess com `capture_output=True` e `text=True` e retornar a lista de caminhos relativos dos arquivos modificados.
2. WHEN `get_changed_files()` é invocada dentro de um Git_Repo sem arquivos modificados no Working_Tree, THE Git_Module SHALL retornar uma lista vazia (`[]`).
3. WHEN o Subprocess retorna `returncode != 0`, THE Git_Module SHALL imprimir a mensagem `"Erro: O diretório atual não é um repositório Git."` e encerrar o processo com código de saída `1` via `sys.exit(1)`.
4. THE Git_Module SHALL filtrar todas as linhas vazias do output do `git diff --name-only` antes de retornar a lista de Changed_Files.
5. THE Git_Module SHALL retornar somente caminhos relativos como strings, sem espaços em branco extras nas extremidades de cada entrada.

### Requirement 2: Leitura de Conteúdo de Arquivo

**User Story:** Como desenvolvedor, quero que o KiroSonar leia o conteúdo completo dos arquivos alterados, para que o contexto integral do código seja enviado à LLM junto com o diff.

#### Acceptance Criteria

1. WHEN `read_file_content(file_path)` é invocada com o caminho de um arquivo existente, THE Git_Module SHALL retornar o conteúdo completo do arquivo como uma string com encoding UTF-8.
2. IF `read_file_content(file_path)` é invocada com o caminho de um arquivo inexistente, THEN THE Git_Module SHALL propagar a exceção `FileNotFoundError` sem capturá-la.
3. THE Git_Module SHALL aceitar tanto caminhos relativos quanto absolutos como argumento `file_path` em `read_file_content`.

### Requirement 3: Conformidade de Código

**User Story:** Como tech lead, quero que o módulo siga os padrões do projeto, para que o código seja mantível e consistente com o restante da base de código.

#### Acceptance Criteria

1. THE Git_Module SHALL declarar type hints em todos os parâmetros e retornos de todas as funções públicas.
2. THE Git_Module SHALL conter docstrings no formato Google Style em todas as funções públicas, descrevendo `Args`, `Returns` e `Raises` quando aplicável.
3. THE Git_Module SHALL utilizar exclusivamente módulos da Standard Library do Python (`subprocess`, `sys`, `os`), sem dependências externas.
4. THE Git_Module SHALL ser compatível com Python 3.11 ou superior.
