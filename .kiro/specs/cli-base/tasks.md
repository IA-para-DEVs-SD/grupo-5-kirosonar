# Plano de Implementação: CLI Base

## Overview

Este plano implementa a CLI Base do KiroSonar em Python, seguindo a arquitetura definida no design. A implementação é incremental, começando pela configuração do projeto, seguida pelos módulos core e finalizando com a integração.

## Tasks

- [ ] 1. Configurar estrutura do projeto e dependências
  - [ ] 1.1 Criar pyproject.toml com console_scripts
    - Configurar entry point `kirosonar = "src.cli:main"`
    - Definir dependências: Python >= 3.11
    - Adicionar dependências de teste: pytest, hypothesis
    - _Requirements: 1.1, 1.2_

  - [ ] 1.2 Criar estrutura de diretórios e arquivos __init__.py
    - Criar `backend/src/__init__.py`
    - Criar `backend/tests/__init__.py`
    - _Requirements: 1.1_

- [ ] 2. Implementar módulo config.py
  - [ ] 2.1 Implementar DEFAULT_RULES e load_rules()
    - Definir constante DEFAULT_RULES com regras em Markdown
    - Implementar `load_rules(rules_path: str | None = None) -> str`
    - Usar encoding UTF-8 para leitura de arquivos
    - Retornar DEFAULT_RULES como fallback para caminhos inválidos
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 9.2_

  - [ ]* 2.2 Escrever teste de propriedade para round-trip UTF-8
    - **Property 3: Round-trip de load_rules com UTF-8**
    - **Validates: Requirements 6.3, 6.5**

  - [ ]* 2.3 Escrever teste de propriedade para fallback DEFAULT_RULES
    - **Property 4: Fallback para DEFAULT_RULES em Caminhos Inválidos**
    - **Validates: Requirements 6.4**

  - [ ]* 2.4 Escrever teste de propriedade para retorno não vazio
    - **Property 5: load_rules Nunca Retorna String Vazia**
    - **Validates: Requirements 9.3**

- [ ] 3. Checkpoint - Validar módulo config
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 4. Implementar módulos mock
  - [ ] 4.1 Criar git_module.py mock
    - Implementar `get_changed_files() -> list[str]`
    - Retornar lista fixa `["src/exemplo.py"]`
    - _Requirements: 5.1_

  - [ ] 4.2 Criar ai_service.py mock
    - Implementar `analyze_code(prompt: str) -> str`
    - Retornar Markdown fixo de análise
    - _Requirements: 5.1_

  - [ ] 4.3 Criar report.py mock
    - Implementar `save_report(content: str, path: str) -> None`
    - Imprimir no console
    - _Requirements: 5.1_

  - [ ] 4.4 Criar autofix.py mock
    - Implementar `apply_fix(ai_response: str, file: str) -> None`
    - Imprimir no console
    - _Requirements: 5.1_

- [ ] 5. Implementar módulo cli.py
  - [ ] 5.1 Implementar verificação de versão Python
    - Criar função `_check_python_version() -> None`
    - Verificar `sys.version_info >= (3, 11)`
    - Exibir mensagem de erro com versão atual se incompatível
    - Encerrar com `sys.exit(1)` se versão inválida
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [ ]* 5.2 Escrever teste de propriedade para verificação de versão
    - **Property 1: Verificação de Versão Python**
    - **Validates: Requirements 2.1, 2.2, 2.3**

  - [ ] 5.3 Implementar parser de argumentos
    - Criar função `_create_parser() -> argparse.ArgumentParser`
    - Configurar subcomando `analyze`
    - Adicionar flags `--path` e `--rules` opcionais
    - Configurar help messages em português
    - _Requirements: 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5_

  - [ ] 5.4 Implementar validação de caminho --path
    - Verificar existência do arquivo antes de processar
    - Exibir mensagem de erro se arquivo não existir
    - Encerrar com código 1 se caminho inválido
    - _Requirements: 4.6_

  - [ ]* 5.5 Escrever teste de propriedade para caminhos inválidos
    - **Property 2: Tratamento de Caminhos Inválidos no --path**
    - **Validates: Requirements 4.6**

  - [ ] 5.6 Implementar função main() e orquestração
    - Criar função `main() -> None`
    - Chamar verificação de versão primeiro
    - Parsear argumentos
    - Orquestrar chamadas aos módulos: git_module, config, ai_service, report, autofix
    - Capturar exceções e exibir mensagens amigáveis
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 9.1, 9.4_

  - [ ]* 5.7 Escrever teste de propriedade para tratamento de exceções
    - **Property 6: Tratamento de Exceções dos Módulos**
    - **Validates: Requirements 5.4**

- [ ] 6. Checkpoint - Validar CLI completa
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Garantir conformidade com padrões de código
  - [ ] 7.1 Adicionar type hints e docstrings
    - Verificar type hints em todas as funções públicas
    - Adicionar docstrings no formato Google Style
    - Garantir conformidade PEP 8
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

- [ ] 8. Checkpoint Final - Validação completa
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marcadas com `*` são opcionais e podem ser puladas para MVP mais rápido
- Cada task referencia requisitos específicos para rastreabilidade
- Checkpoints garantem validação incremental
- Testes de propriedade validam propriedades universais de correção
- Testes unitários validam exemplos específicos e edge cases
- Usar `hypothesis` para property-based testing com mínimo de 100 iterações
