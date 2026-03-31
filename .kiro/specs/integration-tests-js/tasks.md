# Implementation Plan: Integration Tests JS

## Overview

Implementação de uma suite de testes de integração para validar a detecção de erros JavaScript pelo KiroSonar. A implementação consiste em criar um projeto JavaScript de exemplo com erros intencionais e 10 testes de integração em pytest.

## Tasks

- [x] 1. Criar estrutura do projeto JavaScript de teste
  - [x] 1.1 Criar diretório `backend/tests/js-project/src/` e arquivo `package.json`
    - Criar estrutura de diretórios
    - Criar package.json com metadados básicos do projeto
    - _Requirements: 1.1, 1.4_

  - [x] 1.2 Criar arquivos JavaScript com erros de variáveis e código morto
    - Criar `unused_vars.js` com variáveis não utilizadas
    - Criar `unreachable_code.js` com código após return
    - _Requirements: 1.2, 1.3_

  - [x] 1.3 Criar arquivos JavaScript com erros de duplicação e segurança
    - Criar `duplicate_code.js` com blocos duplicados
    - Criar `security_issues.js` com uso de eval()
    - _Requirements: 1.2, 1.3_

  - [x] 1.4 Criar arquivos JavaScript com code smells
    - Criar `code_smells.js` com função longa (>50 linhas)
    - Criar `comparisons.js` com == ao invés de ===
    - Criar `console_logs.js` com console.log
    - _Requirements: 1.2, 1.3_

  - [x] 1.5 Criar arquivos JavaScript com erros de escopo e callbacks
    - Criar `global_vars.js` com variáveis globais implícitas
    - Criar `callback_hell.js` com callbacks aninhados (>3 níveis)
    - Criar `error_handling.js` com try sem catch
    - _Requirements: 1.2, 1.3_

- [x] 2. Checkpoint - Verificar estrutura do projeto de teste
  - Ensure all test project files exist, ask the user if questions arise.

- [x] 3. Implementar testes de integração
  - [x] 3.1 Criar arquivo de testes com helper function
    - Criar `backend/tests/test_integration_js.py`
    - Implementar função `run_kirosonar_analyze()` para executar CLI
    - _Requirements: 12.1_

  - [x] 3.2 Implementar testes de detecção de variáveis e código morto
    - Implementar `test_detects_unused_variables()`
    - Implementar `test_detects_unreachable_code()`
    - _Requirements: 2.1, 3.1, 12.3_

  - [x] 3.3 Implementar testes de detecção de duplicação e segurança
    - Implementar `test_detects_duplicate_code()`
    - Implementar `test_detects_security_vulnerability()`
    - _Requirements: 4.1, 5.1, 12.3_

  - [x] 3.4 Implementar testes de detecção de code smells
    - Implementar `test_detects_long_function()`
    - Implementar `test_detects_loose_equality()`
    - Implementar `test_detects_console_log()`
    - _Requirements: 6.1, 7.1, 8.1, 12.3_

  - [x] 3.5 Implementar testes de detecção de escopo e callbacks
    - Implementar `test_detects_implicit_global()`
    - Implementar `test_detects_callback_hell()`
    - Implementar `test_detects_missing_error_handling()`
    - _Requirements: 9.1, 10.1, 11.1, 12.3_

- [x] 4. Checkpoint - Verificar execução dos testes
  - Ensure all tests pass with `pytest backend/tests/test_integration_js.py -v`, ask the user if questions arise.

## Notes

- Os testes verificam se termos relacionados ao erro aparecem no output do KiroSonar (case-insensitive)
- Termos aceitos incluem variações em inglês e português
- Cada teste executa `kirosonar analyze --path <file>` via subprocess
- A estrutura segue o padrão existente em `backend/tests/`
