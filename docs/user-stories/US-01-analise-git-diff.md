# US-01: Análise automática dos arquivos alterados via Git Diff

## Descrição

> **Como** desenvolvedor que trabalha em um repositório Git,
> **eu quero** executar `kirosonar analyze` no terminal
> **para que** apenas os arquivos que eu modifiquei sejam analisados automaticamente pela IA, sem precisar indicar cada arquivo manualmente.

## Contexto

Este é o fluxo principal do KiroSonar. A filosofia "Clean as You Code" determina que a análise deve ser cirúrgica — focada apenas no que mudou, não no repositório inteiro. Isso reduz custo de tokens, tempo de execução e fricção para o desenvolvedor.

## Critérios de Aceite

- [ ] Ao rodar `kirosonar analyze` dentro de um repositório Git, o sistema executa `git diff --name-only` e identifica os arquivos alterados.
- [ ] Para cada arquivo alterado, o código é lido, combinado com as regras da empresa e enviado à LLM.
- [ ] Um relatório em Markdown é gerado na pasta `relatorios/` com as seções: Bugs, Vulnerabilidades, Code Smells e Hotspots de Segurança.
- [ ] Se não houver arquivos alterados, o sistema exibe a mensagem "Nenhum arquivo alterado encontrado." e encerra sem erro.
- [ ] Se o diretório não for um repositório Git, o sistema exibe mensagem de erro e encerra com código 1.
- [ ] O usuário pode analisar um arquivo específico via `--path src/arquivo.py`, ignorando o git diff.

## Módulos Envolvidos

| Módulo | Responsabilidade |
|---|---|
| `src/cli.py` | Orquestração do fluxo e parsing de argumentos |
| `src/git_module.py` | Execução do `git diff --name-only` e leitura de arquivos |
| `src/config.py` | Carregamento das regras de análise |
| `src/prompt_builder.py` | Montagem do prompt com código + regras |
| `src/ai_service.py` | Envio do prompt à LLM via `kiro-cli` |
| `src/report.py` | Persistência do relatório em `/relatorios` |

## Fluxo

```
kirosonar analyze
    → git diff --name-only
    → para cada arquivo:
        → read_file_content()
        → load_rules()
        → build_prompt(code, rules, file_path)
        → call_llm(prompt)
        → save_report(response, file_path)
```

## Notas Técnicas

- O comando `git diff --name-only` retorna apenas arquivos no working tree (não staged). Isso é intencional para o MVP.
- A variável de ambiente `KIROSONAR_MOCK=1` permite testar o fluxo completo sem uma LLM real.
