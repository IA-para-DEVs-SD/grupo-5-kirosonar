# KiroSonar

Code Review Inteligente e Auto-Fix com IA diretamente no seu terminal. O KiroSonar é uma CLI nativa em Python que atua como um "SonarQube tunado com IA", operando sob a filosofia *"Clean as You Code"*. Em vez de apenas apontar erros em um dashboard web, ele analisa o seu `git diff`, envia para uma LLM avaliar com base nas regras da sua empresa e aplica a refatoração automaticamente no seu código.

---

## Sumário de Documentações

- [RFC 001: Arquitetura MVP](./backend/docs/RFC-001-KiroSonar-MVP.md)
- [Padrão de Projeto](./backend/docs/padrao-projeto.md)
- [Tickets de Desenvolvimento (Backend)](./backend/docs/tickets/)
- [User Stories (Frontend)](./frontend/docs/user-stories/)
- [Code Reviews (Frontend)](./frontend/docs/code-review/)

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
pip install -e .
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

## Integrantes do Grupo 5

- Lucas Braga
- Lucas Heideric
- Matheus Costa
- Matheus Gomes
- Pedro Lima
- Weslley