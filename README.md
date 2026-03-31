# KiroSonar

Code Review Inteligente e Auto-Fix com IA diretamente no seu terminal. O KiroSonar é uma CLI nativa em Python que atua como um "SonarQube tunado com IA", operando sob a filosofia *"Clean as You Code"*. Em vez de apenas apontar erros em um dashboard web, ele analisa o seu `git diff`, envia para uma LLM avaliar com base nas regras da sua empresa e aplica a refatoração automaticamente no seu código.

---

## Arquitetura

```mermaid
flowchart TD
    A[Desenvolvedor executa\nkirosonar analyze] --> B{--path fornecido?}
    B -- Sim --> C[Lê arquivo específico]
    B -- Não --> D[git_module\ngit diff --name-only]
    D --> E[Lista de arquivos alterados]
    E --> F[Para cada arquivo]
    C --> F
    F --> G[git_module\ngit diff arquivo]
    F --> H[git_module\nLê conteúdo completo]
    G --> I[prompt_builder\nMonta prompt com diff + código + regras]
    H --> I
    I --> J[ai_service\nEnvia para LLM via kiro-cli]
    J --> K[report\nSalva relatório .md em /relatorios]
    K --> L[autofix\nExtrai código refatorado]
    L --> M{Usuário aceita fix? s/n}
    M -- Sim --> N[Sobrescreve arquivo original]
    M -- Não --> O[Mantém arquivo original]
```

### Estrutura de Módulos

```
backend/src/
├── cli.py            # Ponto de entrada, orquestra o fluxo completo
├── config.py         # Carrega regras de análise (arquivo ou default)
├── git_module.py     # Integração com Git (diff, arquivos alterados)
├── ai_service.py     # Chamada à LLM via kiro-cli (subprocess)
├── prompt_builder.py # Montagem do prompt estruturado para a LLM
├── report.py         # Geração e salvamento de relatórios Markdown
└── autofix.py        # Extração e aplicação do código refatorado
```

---

## Sumário de Documentações

- [RFC 001: Arquitetura MVP](./backend/docs/RFC-001-KiroSonar-MVP.md)
- [Tickets de Desenvolvimento](./backend/docs/tickets/)
- [User Stories](./backend/docs/user-stories/)
- [Code Reviews](./backend/docs/code-review/)
- [Padrão de Projeto](./backend/docs/padrao-projeto.md)
- [Tickets de Desenvolvimento (Backend)](./backend/docs/tickets/)

---

## Tecnologias Utilizadas

- Python 3.11+
- Bibliotecas nativas (Standard Library): `argparse`, `subprocess`, `os`, `re`, `sys`
- Git (para captura de diffs)
- LLM via `kiro-cli` (IA local/remota)
- Setuptools (empacotamento via `pyproject.toml`)
- Conda (gerenciamento de ambiente)

---

## Instruções de Instalação e Uso

### Pré-requisitos

- Python 3.11 ou superior
- Git instalado
- Binário `kiro-cli` disponível no PATH

### Instalação

```bash
pip install KiroSonar
```

### Configuração do Ambiente de Desenvolvimento

```bash
conda create -n kirosonar python=3.11 -y
conda activate kirosonar
pip install -e ".[dev]"
```

### Uso

```bash
# Analisa automaticamente todos os arquivos alterados no repositório local
kirosonar analyze

# Analisa um arquivo específico, ignorando o git diff
kirosonar analyze --path src/meu_arquivo.py

# Especifica um arquivo de regras customizado
kirosonar analyze --rules caminho/para/regras.md
```

### Regras Personalizadas

Crie um arquivo `regras_empresa.md` na raiz do seu projeto com as diretrizes de código do seu time. O KiroSonar lerá esse arquivo automaticamente e usará as regras para avaliar o código. Caso o arquivo não exista, regras padrão serão utilizadas.

---

## Variáveis de Ambiente

| Variável | Descrição | Valores | Default |
|---|---|---|---|
| `KIROSONAR_MOCK` | Ativa mock da LLM para testes offline | `1` (mock) / `0` (real) | `0` (real) |

Copie o arquivo de exemplo e ajuste conforme necessário:

```bash
cp backend/.env.example backend/.env
```

---

## Fluxo de Dados

1. O usuário executa `kirosonar analyze` (com ou sem `--path`)
2. O módulo `git_module` descobre arquivos alterados via `git diff --name-only`
3. Para cada arquivo, captura o diff e o conteúdo completo
4. O `prompt_builder` monta um prompt estruturado com diff (peso máximo), código completo (peso médio) e regras da empresa
5. O `ai_service` envia o prompt para a LLM via `kiro-cli` (subprocess com timeout de 120s)
6. A resposta é salva como relatório Markdown em `/relatorios`
7. O `autofix` extrai código refatorado (entre tags `[START]`/`[END]`) e oferece aplicação interativa

---

## Troubleshooting

**"Erro: o diretório atual não é um repositório Git válido."**
Certifique-se de estar na raiz de um repositório Git inicializado (`git init`).

**"Erro: KiroSonar requer Python 3.11 ou superior."**
Verifique sua versão com `python3 --version`. Use `conda` ou `pyenv` para instalar a versão correta.

**"Timeout: kiro-cli não respondeu em 120 segundos."**
Verifique se o `kiro-cli` está instalado e acessível no PATH. Teste com `kiro-cli --version`.

**"Nenhum arquivo alterado encontrado."**
Isso significa que `git diff --name-only` não retornou nada. Verifique se há alterações não commitadas com `git status`. Alternativamente, use `--path` para analisar um arquivo específico.

**"Nenhum código refatorado encontrado na resposta da IA."**
A LLM não retornou código entre as tags `[START]`/`[END]`. Isso pode acontecer se a IA não encontrou necessidade de refatoração ou se o prompt foi muito grande.

---

## Integrantes do Grupo 5

- Lucas Braga
- Lucas Heideric
- Matheus Costa
- Matheus Gomes
- Pedro Lima
- Weslley