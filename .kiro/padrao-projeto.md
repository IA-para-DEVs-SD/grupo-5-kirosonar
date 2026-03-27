## Diretrizes da organização

### Estrutura de repositórios da organização

```
meu-projeto/
├── .kiro/                  # Especificações do Kiro/IA
├── .github/                # Especificações e configurações para Github
├── [backend/frontend]/     # Monorepo podendo ser backend e front 
│   ├── docs/               # Documentações
│   ├── tests/              # Testes automatizados
│   ├── src/                # Diretórios com códigos do monorepo
│   ├──.env.example         # Variáveis de ambiente 
├── scripts/                # Opcional: Scripts gerais do repositório
├── Dockerfile              # Opcional: Imagem Docker
├── docker-compose.yml      # Opcional: Orquestração para rodar local
└── README.md               # Documentação inicial do projeto
└── .gitignore              # Ignora arquivos e pastas no versionamento
```

### Estrutura padrão de repositórios

Padrão de nomenclatura dos repositórios de projetos
- Nome grupo + Nome do projeto: Exemplo: "grupo-x-nome-projeto"
- Não utilizar caracteres especiais além do hífen
- Texto sempre em minúsculo

Padrão de nomenclatura dos repositórios de atividades
- Nome grupo + Atividades + Nome aluno: Exemplo: "grupo-x-atividades-fulano-sobrenome"
- Não utilizar caracteres especiais além do hífen
- Texto sempre em minúsculo
 
Padrão do Gitflow
- Branch principal: main
- Branch desenvolvimento: develop
- Branch de novas funcionalidades: feature/issue-xxx

Padrão do commit semântico

"tipo: breve descrição

descrição mais detalhada (opcional)"

Tipos:
- feat: Nova funcionalidade
- docs: Documentações
- fix: Correções
- refactor: Refatorações
- tests: Testes unitários, etc
  
Padrão de nomenclatura dos boards / projetos
- Identificação do Grupo + Nome do Projeto
- Exemplo: "Grupo X - Nome Projeto"

Padrão de tópicos do README
- Nome do Projeto
- Breve descrição do projeto
- Sumário de documentações
- Tecnologias utilizadas
- Instruções de instalação / uso
- Integrantes do grupo
  
