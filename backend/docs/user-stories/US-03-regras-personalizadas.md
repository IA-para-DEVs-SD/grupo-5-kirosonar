# US-03: Personalização das regras de análise por projeto

## Descrição

> **Como** tech lead de um time de desenvolvimento,
> **eu quero** criar um arquivo `regras_empresa.md` com as diretrizes de código do meu time
> **para que** a IA avalie o código com base nos padrões específicos da minha organização, e não apenas em boas práticas genéricas.

## Contexto

Cada time tem suas próprias convenções: naming, limites de complexidade, padrões arquiteturais, etc. O KiroSonar permite que essas regras sejam escritas em linguagem natural (Markdown), tornando-as acessíveis para qualquer membro do time — sem necessidade de configurar XMLs ou JSONs complexos como em ferramentas tradicionais.

## Critérios de Aceite

- [ ] Se existir um arquivo `regras_empresa.md` na raiz do projeto, o sistema carrega seu conteúdo e injeta no prompt enviado à LLM.
- [ ] Se o arquivo não existir, o sistema utiliza um conjunto de regras padrão (`DEFAULT_RULES`) como fallback, sem interromper a execução.
- [ ] O usuário pode especificar um caminho alternativo para o arquivo de regras via `--rules <caminho>`.
- [ ] As regras são escritas em linguagem natural (Markdown), permitindo que qualquer membro do time as edite sem conhecimento técnico avançado.
- [ ] As `DEFAULT_RULES` cobrem boas práticas genéricas: SOLID, naming, complexidade, type hints, DRY, docstrings.

## Módulos Envolvidos

| Módulo | Responsabilidade |
|---|---|
| `src/config.py` | Carregamento do arquivo de regras ou fallback para `DEFAULT_RULES` |
| `src/prompt_builder.py` | Injeção das regras no prompt enviado à LLM |
| `src/cli.py` | Passagem do argumento `--rules` para `load_rules()` |

## Fluxo

```
kirosonar analyze [--rules caminho/regras.md]
    → load_rules(rules_path)
        → se --rules fornecido: lê o arquivo indicado
        → se não: busca regras_empresa.md na raiz
        → se não encontrou: retorna DEFAULT_RULES
    → build_prompt(code, rules, file_path)
        → regras injetadas na seção "Regras da Empresa" do prompt
```

## Exemplo de `regras_empresa.md`

```markdown
# Regras do Time Backend

- Todas as funções públicas devem ter docstrings com Args e Returns.
- Limite máximo de 15 linhas por função.
- Proibido uso de `print()` em código de produção — usar logging.
- Nomes de variáveis em inglês, sempre descritivos.
- Toda exceção deve ser tratada explicitamente (nunca bare except).
- Imports devem seguir a ordem: stdlib → third-party → local.
- Proibido uso de `Any` como type hint sem justificativa em comentário.
```

## Notas Técnicas

- O `DEFAULT_RULES` contém ~10 regras genéricas de código limpo como fallback seguro.
- O arquivo de regras é lido uma única vez por execução e reutilizado para todos os arquivos analisados.
- Encoding esperado: UTF-8.
