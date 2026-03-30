# Plano de Implementação: report-module

## Visão Geral

Implementação do módulo `report.py` do KiroSonar, responsável por gerar nomes únicos de relatório e persistir conteúdo Markdown em `relatorios/`. O módulo usa apenas Standard Library Python e é completamente independente dos demais módulos do projeto.

## Tasks

- [ ] 1. Implementar `generate_report_name` em `backend/src/report.py`
  - Adicionar a constante `MOCK_CONTENT` com string Markdown fixa para testes independentes
  - Implementar sanitização de `file_path` substituindo `/`, `\` e `.` por `_` → `safe_name`
  - Capturar timestamp com `datetime.now().strftime("%Y%m%d_%H%M%S")`
  - Retornar `os.path.join("relatorios", f"{safe_name}_{timestamp}.md")`
  - Adicionar type hints e docstring completa
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ] 2. Implementar `save_report` em `backend/src/report.py`
  - [ ] 2.1 Implementar corpo da função `save_report`
    - Chamar `generate_report_name(file_path)` para obter `report_name`
    - Criar diretório com `os.makedirs(os.path.dirname(report_name), exist_ok=True)`
    - Escrever `content` no arquivo com `open(..., "w", encoding="utf-8")`
    - Imprimir caminho absoluto em `stdout` via `print()`
    - Retornar `os.path.abspath(report_name)`
    - Adicionar type hints e docstring completa
    - _Requirements: 2.1, 2.2, 3.1, 3.2, 3.4, 4.1, 4.2, 6.1_

  - [ ]* 2.2 Escrever testes unitários para `generate_report_name`
    - Testar exemplo concreto: `"src/app.py"` → prefixo `relatorios/`, sufixo `.md`, `safe_name` sem `/` nem `.`
    - Testar `file_path` com separador Windows `\`
    - Testar `file_path` vazio `""` (comportamento definido, sem exceção)
    - Usar `monkeypatch` para fixar `datetime.now()` e verificar formato do timestamp
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [ ]* 2.3 Escrever testes unitários para `save_report`
    - Testar criação do arquivo com `MOCK_CONTENT` usando `tmp_path`
    - Testar que `relatorios/` já existente não lança exceção (idempotência)
    - Testar `content` vazio `""` cria arquivo sem erro
    - Testar que o retorno é caminho absoluto apontando para arquivo existente
    - Testar que `stdout` contém o caminho absoluto (capturar com `capsys`)
    - _Requirements: 2.1, 2.2, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 5.1, 5.2, 6.1_

- [ ] 3. Checkpoint — Garantir que os testes unitários passam
  - Garantir que todos os testes passam, perguntar ao usuário se houver dúvidas.

- [ ] 4. Escrever testes de propriedade com Hypothesis em `backend/tests/test_report.py`
  - [ ]* 4.1 Escrever teste de propriedade para Property 1: Formato do nome gerado
    - `@given(st.text(min_size=1))` — verificar prefixo `"relatorios/"`, sufixo `".md"` e regex `\d{8}_\d{6}` no resultado
    - Tag: `# Feature: report-module, Property 1: Formato do nome gerado`
    - `@settings(max_examples=100)`
    - **Property 1: Formato do nome gerado**
    - **Validates: Requirements 1.1, 1.4**

  - [ ]* 4.2 Escrever teste de propriedade para Property 2: Sanitização do safe_name
    - `@given(st.text())` — verificar ausência de `/`, `\` e `.` na parte `safe_name` do resultado
    - Tag: `# Feature: report-module, Property 2: Sanitização do safe_name`
    - `@settings(max_examples=100)`
    - **Property 2: Sanitização do safe_name**
    - **Validates: Requirements 1.2, 1.3**

  - [ ]* 4.3 Escrever teste de propriedade para Property 3: Diretório criado automaticamente
    - `@given(st.text(), st.text(min_size=1))` com `tmp_path` — verificar que `relatorios/` existe após `save_report`
    - Tag: `# Feature: report-module, Property 3: Diretório criado automaticamente`
    - `@settings(max_examples=100)`
    - **Property 3: Diretório criado automaticamente**
    - **Validates: Requirements 2.1, 2.2**

  - [ ]* 4.4 Escrever teste de propriedade para Property 4: Round-trip de conteúdo com Unicode
    - `@given(st.text())` com `tmp_path` — escrever e ler o arquivo, comparar conteúdo byte a byte
    - Tag: `# Feature: report-module, Property 4: Round-trip de conteúdo com Unicode`
    - `@settings(max_examples=100)`
    - **Property 4: Round-trip de conteúdo com Unicode**
    - **Validates: Requirements 3.1, 3.2, 3.3**

  - [ ]* 4.5 Escrever teste de propriedade para Property 5: Retorno é caminho absoluto existente
    - `@given(st.text(), st.text(min_size=1))` com `tmp_path` — verificar `os.path.isabs` e `os.path.exists`
    - Tag: `# Feature: report-module, Property 5: Retorno é caminho absoluto existente`
    - `@settings(max_examples=100)`
    - **Property 5: Retorno é caminho absoluto existente**
    - **Validates: Requirements 4.1, 4.2**

  - [ ]* 4.6 Escrever teste de propriedade para Property 6: file_paths distintos geram nomes distintos
    - `@given(st.text(), st.text())` com `assume(fp1 != fp2)` — verificar que os `safe_name` diferem
    - Tag: `# Feature: report-module, Property 6: file_paths distintos geram nomes distintos`
    - `@settings(max_examples=100)`
    - **Property 6: file_paths distintos geram nomes distintos**
    - **Validates: Requirements 5.1**

  - [ ]* 4.7 Escrever teste de propriedade para Property 7: stdout contém o caminho absoluto
    - `@given(st.text(), st.text(min_size=1))` com `tmp_path` e `capsys` — verificar que `stdout` contém o caminho retornado
    - Tag: `# Feature: report-module, Property 7: stdout contém o caminho absoluto`
    - `@settings(max_examples=100)`
    - **Property 7: stdout contém o caminho absoluto**
    - **Validates: Requirements 6.1**

- [ ] 5. Checkpoint final — Garantir que todos os testes passam
  - Garantir que todos os testes unitários e de propriedade passam, perguntar ao usuário se houver dúvidas.

## Notas

- Tasks marcadas com `*` são opcionais e podem ser puladas para um MVP mais rápido
- Todos os testes de I/O devem usar `tmp_path` do pytest para isolamento do sistema de arquivos real
- O módulo não deve importar nenhum outro módulo interno do KiroSonar
- `datetime.now()` pode ser mockado com `monkeypatch` para testes de unicidade temporal
- Testes de propriedade requerem `hypothesis` instalado: `pip install hypothesis`
