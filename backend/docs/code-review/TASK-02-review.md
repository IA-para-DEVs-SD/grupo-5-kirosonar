# Guideline de Code Review — TASK-02: Módulo Git Diff

## Arquivo Revisado
`src/git_module.py`

---

## Checklist de Contrato

| Função | Input Esperado | Output Esperado | Validado? |
|---|---|---|---|
| `get_changed_files()` | Nenhum | `list[str]` com paths relativos | [ ] |
| `get_changed_files()` | Nenhum (sem alterações) | `[]` (lista vazia) | [ ] |
| `get_changed_files()` | Nenhum (fora de repo Git) | `sys.exit(1)` com mensagem de erro | [ ] |
| `read_file_content(file_path)` | `str` (path válido) | `str` com conteúdo do arquivo | [ ] |
| `read_file_content(file_path)` | `str` (path inválido) | Levanta `FileNotFoundError` | [ ] |

---

## Pontos Críticos para o Revisor

### 1. `subprocess.run` — Linha ~21
Verificar se os parâmetros `capture_output=True` e `text=True` estão presentes.
Sem eles, o `stdout` retorna `bytes` em vez de `str`, quebrando o `splitlines()`.

### 2. Verificação de `returncode` — Linha ~27
O `returncode != 0` é a única forma de detectar que não estamos em um repo Git.
Confirmar que a mensagem de erro exibida ao usuário é clara e está em Português.

### 3. Filtro de linhas vazias — Linha ~34
O `git diff --name-only` pode retornar uma linha vazia ao final.
Confirmar que a list comprehension com `if line.strip()` está presente para evitar
paths vazios na lista retornada.

### 4. `read_file_content` — encoding UTF-8
Confirmar que `encoding="utf-8"` está explícito no `open()`.
Sem isso, o comportamento varia conforme o sistema operacional (especialmente Windows).

### 5. Política de Idiomas
- Docstrings do módulo e funções: **Inglês** ✅
- Comentários inline (`#`): **Português** ✅
- Mensagens de `print()`: **Português** ✅

---

## Comando de Teste

```bash
pytest tests/test_git_module.py -v
```

---

## Critérios de Aceite (Definition of Done)

- [ ] `get_changed_files()` retorna lista correta dentro de repo com alterações.
- [ ] `get_changed_files()` retorna `[]` dentro de repo sem alterações.
- [ ] `get_changed_files()` chama `sys.exit(1)` fora de um repo Git.
- [ ] `read_file_content()` lê corretamente um arquivo existente.
- [ ] `read_file_content()` levanta `FileNotFoundError` para arquivo inexistente.
- [ ] Código segue PEP 8, tem type hints e docstrings em todas as funções.
- [ ] Todos os testes em `tests/test_git_module.py` passam.
