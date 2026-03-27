# Tasks — git-diff-module

## Task List

- [ ] 1. Implementar `get_changed_files()` em `backend/src/git_module.py`
  - [ ] 1.1 Executar `subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True)`
  - [ ] 1.2 Verificar `returncode != 0`: imprimir `"Erro: O diretório atual não é um repositório Git."` e chamar `sys.exit(1)`
  - [ ] 1.3 Filtrar linhas vazias e aplicar `strip()` em cada linha do output
  - [ ] 1.4 Adicionar type hint `-> list[str]` e docstring Google Style com `Returns` e `Raises`

- [ ] 2. Implementar `read_file_content()` em `backend/src/git_module.py`
  - [ ] 2.1 Abrir arquivo com `open(file_path, encoding="utf-8")` e retornar conteúdo completo
  - [ ] 2.2 Não capturar `FileNotFoundError` — propagar para o chamador
  - [ ] 2.3 Adicionar type hint `(file_path: str) -> str` e docstring Google Style com `Args`, `Returns` e `Raises`

- [ ] 3. Escrever testes unitários em `backend/tests/test_git_module.py`
  - [ ] 3.1 Testar `get_changed_files()` retorna lista correta de arquivos (mock subprocess)
  - [ ] 3.2 Testar `get_changed_files()` retorna `[]` quando stdout vazio
  - [ ] 3.3 Testar `get_changed_files()` filtra linhas vazias do output
  - [ ] 3.4 Testar `get_changed_files()` chama `sys.exit(1)` quando `returncode != 0`
  - [ ] 3.5 Testar `get_changed_files()` invoca subprocess com argumentos corretos
  - [ ] 3.6 Testar `read_file_content()` retorna conteúdo de arquivo existente
  - [ ] 3.7 Testar `read_file_content()` levanta `FileNotFoundError` para arquivo inexistente

- [ ] 4. Escrever testes de propriedade em `backend/tests/test_git_module_properties.py`
  - [ ] 4.1 Property 1: output parsing preserva apenas entradas válidas (hypothesis, 100 exemplos)
  - [ ] 4.2 Property 2: qualquer returncode não-zero resulta em SystemExit(1) (hypothesis, 100 exemplos)
  - [ ] 4.3 Property 3: leitura de arquivo é round-trip fiel (hypothesis + tmp_path, 100 exemplos)
  - [ ] 4.4 Property 4: equivalência entre caminhos relativos e absolutos (hypothesis + tmp_path, 100 exemplos)

- [ ] 5. Verificar conformidade de código
  - [ ] 5.1 Executar `ruff check backend/src/git_module.py` sem erros
  - [ ] 5.2 Executar `mypy backend/src/git_module.py` sem erros de tipo
  - [ ] 5.3 Confirmar que o módulo importa apenas `subprocess`, `sys` e `os`
