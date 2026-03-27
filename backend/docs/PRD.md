# PRD: KiroSonar — Code Review e Auto-Fix com IA

**Versão:** 1.0 (MVP)
**Status:** Em rascunho
**Data:** 25 de março de 2026
**Referência:** RFC-001-KiroSonar-MVP.md

---

## 1. Visão Geral

KiroSonar é uma CLI em Python que integra análise estática de código baseada em IA e refatoração automática (Auto-Fix) diretamente no terminal do desenvolvedor. O objetivo é eliminar a fricção do ciclo tradicional de code review, onde o desenvolvedor precisa consultar dashboards externos e reescrever código manualmente.

---

## 2. Problema

Ferramentas como o SonarQube operam de forma passiva e desconectada do fluxo de trabalho do desenvolvedor:

- A análise ocorre em um dashboard externo, exigindo mudança de contexto.
- O desenvolvedor recebe o feedback tarde demais no ciclo de desenvolvimento.
- A correção é sempre manual, sem sugestão de refatoração automatizada.
- Não há integração com o fluxo Git local ("Clean as You Code").

---

## 3. Solução

Uma CLI (`kirosonar`) que:

1. Detecta automaticamente os arquivos alterados via `git diff`.
2. Envia o código para uma LLM junto com as regras de qualidade do time.
3. Gera um relatório estruturado (Bugs, Vulnerabilidades, Code Smells, Hotspots).
4. Oferece ao desenvolvedor a opção de aplicar o Auto-Fix com aprovação explícita.

---

## 4. Usuários-Alvo

| Persona | Necessidade |
|---|---|
| Desenvolvedor Fullstack | Receber feedback de qualidade em qualquer camada da aplicação sem sair do terminal |
| Tech Lead | Garantir que o time siga os padrões arquiteturais do projeto via regras personalizadas |
| Analista de Qualidade | Identificar bugs, vulnerabilidades e code smells de forma automatizada antes do merge |

---

## 5. Requisitos Funcionais

### RF-01: Análise via Git Diff + Arquivo Completo
- Ao executar `kirosonar analyze`, o sistema identifica os arquivos alterados via `git diff --name-only`.
- Para cada arquivo identificado, duas entradas distintas são enviadas à LLM no mesmo prompt:
  - **Diff (peso máximo):** as alterações recentes ainda não comitadas, obtidas via `git diff <arquivo>`. Esta seção recebe prioridade máxima na análise — é o foco principal do review.
  - **Arquivo completo (peso médio):** o conteúdo integral do arquivo, fornecido como contexto para que a IA compreenda o impacto das mudanças no todo. Esta seção tem peso secundário na análise.
- A separação entre diff e arquivo completo deve ser explícita no prompt, com instruções claras de ponderação para a LLM.
- Um relatório em Markdown é gerado em `relatorios/` com as seções: Bugs, Vulnerabilidades, Code Smells e Hotspots de Segurança.
- Se não houver arquivos alterados, exibe "Nenhum arquivo alterado encontrado." e encerra sem erro.
- Se o diretório não for um repositório Git, exibe mensagem de erro e encerra com código 1.
- O usuário pode analisar um arquivo específico via `--path src/arquivo.py`, ignorando o git diff.

### RF-02: Auto-Fix Interativo
- Se a resposta da IA contiver código refatorado entre as tags `[START]` e `[END]`, o sistema exibe um preview das primeiras 20 linhas no terminal.
- O sistema pergunta: `"Deseja aplicar o fix em '<arquivo>'? (s/n)"`.
- Se `s`: o arquivo original é sobrescrito com o código refatorado (encoding UTF-8).
- Se qualquer outra entrada: o fix não é aplicado e o sistema informa "Fix não aplicado."
- Se a resposta da IA não contiver as tags, o sistema informa que não há código refatorado e segue sem erro.
- O arquivo original só é alterado após confirmação explícita — nunca automaticamente.

### RF-03: Regras de Análise Personalizáveis
- Se existir `regras_empresa.md` na raiz do projeto, o sistema carrega seu conteúdo e injeta no prompt enviado à LLM.
- Se o arquivo não existir, o sistema utiliza `DEFAULT_RULES` como fallback, sem interromper a execução.
- O usuário pode especificar um caminho alternativo via `--rules <caminho>`.
- As regras são escritas em linguagem natural (Markdown).
- As `DEFAULT_RULES` cobrem: SOLID, naming, complexidade, type hints, DRY, docstrings.

---

## 6. Requisitos Não-Funcionais

| Requisito | Descrição |
|---|---|
| Linguagem | Python 3.11+ com verificação de versão no startup ("Fail Fast") |
| Node.js | v24.x LTS (Active LTS — codinome "Krypton") |
| npm | v11.x (bundled com Node.js 24 LTS) |
| Git | v2.x+ (necessário para execução do `git diff`) |
| Distribuição | Executável de sistema via `pyproject.toml` (`console_scripts`) — sem prefixo `python` |
| Dependências | Apenas Standard Library (`argparse`, `subprocess`, `os`, `re`, `sys`) |
| Padrões de código | PEP 8, Type Hinting obrigatório, Docstrings, SOLID, Clean Architecture |
| Encoding | UTF-8 em todas as operações de leitura/escrita de arquivos |
| Testabilidade | Variável `KIROSONAR_MOCK=1` para simular LLM em testes |

---

## 7. User Stories

| ID | Descrição |
|---|---|
| US-01 | Como desenvolvedor, quero executar `kirosonar analyze` para que apenas os arquivos que modifiquei sejam analisados automaticamente pela IA. |
| US-02 | Como desenvolvedor, quero visualizar um preview do código refatorado e decidir se aplico ou não a correção. |
| US-03 | Como tech lead, quero criar um arquivo `regras_empresa.md` para que a IA avalie o código com base nos padrões do meu time. |

---

## 8. Arquitetura de Módulos

| Módulo | Responsabilidade |
|---|---|
| `src/cli.py` | Orquestração do fluxo e parsing de argumentos (`argparse`) |
| `src/git_module.py` | Execução do `git diff --name-only`, captura do diff por arquivo (`git diff <arquivo>`) e leitura do conteúdo completo |
| `src/config.py` | Carregamento das regras de análise ou fallback para `DEFAULT_RULES` |
| `src/prompt_builder.py` | Montagem do prompt com diff (peso máximo) + arquivo completo (peso médio) + regras |
| `src/ai_service.py` | Envio do prompt à LLM |
| `src/report.py` | Persistência do relatório em `/relatorios` |
| `src/autofix.py` | Extração do código refatorado e aplicação com confirmação interativa |

---

## 9. Fluxo Principal

```
kirosonar analyze [--path arquivo] [--rules regras.md]
    → verifica versão Python (>= 3.11)
    → git diff --name-only  (ou usa --path)
    → load_rules()          (regras_empresa.md ou DEFAULT_RULES)
    → para cada arquivo:
        → git diff <arquivo>        → diff das alterações não comitadas (peso máximo)
        → read_file_content()       → conteúdo completo do arquivo (peso médio)
        → build_prompt(diff, full_code, rules, file_path)
        → call_llm(prompt)
        → save_report(response, file_path)  → relatorios/
        → extract_refactored_code(response)
            → se encontrou [START]...[END]:
                → exibe preview (20 linhas)
                → "Deseja aplicar o fix? (s/n)"
                → se 's': sobrescreve arquivo
```

---

## 10. Critérios de Aceitação (MVP)

- [ ] `kirosonar analyze` executa sem o prefixo `python`.
- [ ] Arquivos alterados são detectados automaticamente via `git diff`.
- [ ] O prompt enviado à LLM contém o diff (peso máximo) e o arquivo completo (peso médio) de forma separada e explicitamente ponderada.
- [ ] Relatório gerado em `relatorios/` com as 4 seções (Bugs, Vulnerabilidades, Code Smells, Hotspots).
- [ ] Auto-Fix só é aplicado após confirmação explícita do usuário.
- [ ] Regras customizadas via `regras_empresa.md` são injetadas no prompt.
- [ ] Fallback para `DEFAULT_RULES` quando o arquivo de regras não existe.
- [ ] Mensagens de erro claras para repositório Git inválido ou ausência de arquivos alterados.
- [ ] Todos os módulos com Type Hinting e Docstrings.

---

## 11. Fora do Escopo (MVP)

- Integração com CI/CD na nuvem (GitHub Actions / GitLab CI).
- Dashboard Web.
- Análise de repositórios inteiros sem `git diff` ou `--path`.
- Mecanismo de rollback automático (o desenvolvedor usa `git checkout` para reverter).

---

## 12. Riscos e Mitigações

| Risco | Mitigação |
|---|---|
| Custo elevado de tokens | O diff foca nas alterações recentes; o arquivo completo é enviado como contexto secundário — o prompt deve ser estruturado para minimizar tokens redundantes |
| Alucinação da IA gerando código incorreto | Aprovação humana explícita `(s/n)` obrigatória antes de qualquer sobrescrita |
| Dependência de LLM externa | Variável `KIROSONAR_MOCK=1` permite execução offline para testes |

---

## 13. Métricas de Sucesso

- Tempo médio entre `kirosonar analyze` e relatório gerado < 30 segundos.
- Taxa de aceitação do Auto-Fix pelos desenvolvedores > 60%.
- Zero sobrescritas de arquivo sem confirmação explícita do usuário.