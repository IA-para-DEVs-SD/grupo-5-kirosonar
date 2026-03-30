# Plano de Implementação: autofix-module

## Visão Geral

Implementação do módulo `autofix.py` do KiroSonar, responsável por extrair o código refatorado da resposta da LLM e aplicá-lo ao arquivo original com confirmação explícita do usuário. O módulo usa apenas Standard Library Python e é completamente independente dos demais módulos do projeto.

O arquivo `backend/src/autofix.py` já possui uma implementação inicial. As tasks abaixo cobrem a verificação, ajustes necessários e a escrita dos testes.

## Tasks

- [ ] 1. Verificar e validar `extract_refactored_code` em `backend/src/autofix.py`
  - Confirmar que o Regex `r'\[START\]\s*\n(.*?)\n\s*\[END\]'` está aplicado com a flag `re.DOTALL`
  - Confirmar que retorna `match.group(1)` quando as tags são encontradas
  - Confirmar que retorna `None` quando as tags estão ausentes
  - Confirmar type hints (`ai_response: str`) e retorno (`str | None`)
  - Confirmar docstring completa com Args e Returns
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ] 2. Verificar e validar `apply_fix` em `backend/src/autofix.py`
  - Confirmar que chama `extract_refactored_code()` e retorna `False` se `None`
  - Confirmar que exibe o `file_path` e o preview das primeiras 20 linhas via `code.splitlines()[:20]`
  - Confirmar que exibe o prompt `Deseja aplicar o fix em '<file_path>'? (s/n): `
  - Confirmar que aceita `s` e `S` (case-insensitive via `.strip().lower()`)
  - Confirmar que sobrescreve o arquivo com `open(file_path, "w", encoding="utf-8")`
  - Confirmar que retorna `True` após sobrescrita e `False` em caso de recusa ou ausência de código
  - Confirmar type hints e docstring completa
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3_

- [ ] 3. Adicionar `MOCK_AI_RESPONSE` em `backend/src/autofix.py`
  - Adicionar a constante `MOCK_AI_RESPONSE` com a string Markdown definida na TASK-05
  - Garantir que o mock contém as tags `[START]` e `[END]` com código válido
  - _Requirements: 1.5, 6.1_

- [ ] 4. Escrever testes unitários para `extract_refactored_code` em `backend/tests/test_autofix.py`
  - [ ]* 4.1 Testar extração com `MOCK_AI_RESPONSE` → retorna o código correto
  - [ ]* 4.2 Testar extração com código multilinhas → retorna todas as linhas
  - [ ]* 4.3 Testar sem tags → retorna `None`
  - [ ]* 4.4 Testar apenas `[START]` sem `[END]` → retorna `None`
  - [ ]* 4.5 Testar código vazio entre as tags → retorna string vazia ou `None` conforme o Regex
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ] 5. Escrever testes unitários para `apply_fix` em `backend/tests/test_autofix.py`
  - [ ]* 5.1 Testar sem código refatorado → retorna `False`, nenhum arquivo criado (`tmp_path`)
  - [ ]* 5.2 Testar com código, usuário digita `n` → retorna `False`, arquivo não modificado (mock `input`)
  - [ ]* 5.3 Testar com código, usuário digita `s` → retorna `True`, arquivo sobrescrito com conteúdo correto
  - [ ]* 5.4 Testar com código, usuário digita `S` → retorna `True` (case-insensitive)
  - [ ]* 5.5 Testar com código, usuário digita entrada vazia → retorna `False`
  - [ ]* 5.6 Testar preview limitado a 20 linhas para código com mais de 20 linhas (capturar `stdout` com `capsys`)
  - [ ]* 5.7 Testar que a mensagem de aviso é exibida quando não há código refatorado (`capsys`)
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3_

- [ ] 6. Checkpoint final — Garantir que todos os testes passam
  - Executar `pytest backend/tests/test_autofix.py -v` e confirmar que todos os testes passam
  - Garantir que o módulo segue PEP 8 (sem imports desnecessários, indentação correta)
  - Perguntar ao usuário se houver dúvidas antes de encerrar

## Notas

- Tasks marcadas com `*` são opcionais e podem ser puladas para um MVP mais rápido
- Todos os testes de I/O devem usar `tmp_path` do pytest para isolamento do sistema de arquivos real
- Usar `monkeypatch` para mockar `builtins.input` nos testes de `apply_fix`
- Usar `capsys` para verificar mensagens exibidas no terminal
- O módulo não deve importar nenhum outro módulo interno do KiroSonar
- A implementação atual em `autofix.py` já cobre os requisitos principais — as tasks 1 e 2 são de verificação/validação
