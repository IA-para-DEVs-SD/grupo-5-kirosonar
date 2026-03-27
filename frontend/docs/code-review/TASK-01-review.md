# Code Review — TASK-01: CLI Base, Entry Point e Configuração

## Checklist de Contrato

| Função | Input Esperado | Output Esperado | Validado? |
|---|---|---|---|
| `main()` | `None` (lê `sys.argv`) | `None` (orquestra chamadas ou imprime help) | ⬜ |
| `_build_parser()` | `None` | `argparse.ArgumentParser` com subcomando `analyze` | ⬜ |
| `_run_analyze(args)` | `argparse.Namespace` com `.path` e `.rules` | `None` (executa fluxo de análise com prints) | ⬜ |
| `load_rules(rules_path)` | `str \| None` | `str` (conteúdo das regras ou `DEFAULT_RULES`) | ⬜ |

## Pontos Críticos para o Revisor

1. **`src/cli.py` — Linhas 17-22 (Fail-Fast de versão):**
   - A checagem roda no nível do módulo (fora de função). Isso é intencional para barrar a execução antes de qualquer import falhar em Python < 3.11.
   - Verificar que a mensagem de erro está clara e que `sys.exit(1)` é chamado.

2. **`src/cli.py` — Mocks temporários (linhas 29-48):**
   - São funções prefixadas com `_mock_` que serão substituídas pelos imports reais nas TASK-02 a TASK-05.
   - O revisor deve garantir que os contratos (assinaturas) batem com o que está definido na TASK-01.

3. **`src/config.py` — `load_rules()` (linha 26):**
   - Usa `os.getcwd()` para resolver o caminho padrão. Isso significa que o arquivo `regras_empresa.md` é buscado no diretório de onde o usuário executa o comando, não no diretório do projeto.
   - Verificar se esse comportamento é o desejado pelo time.

4. **Política de Idiomas:**
   - Nomes de variáveis, funções, classes e docstrings devem estar em **inglês**.
   - Comentários de código e prints no console devem estar em **português Brasil**.

## Comando de Teste

```bash
pytest tests/test_cli.py tests/test_config.py -v
```
