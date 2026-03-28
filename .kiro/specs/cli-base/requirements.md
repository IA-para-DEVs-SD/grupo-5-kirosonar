# Documento de Requisitos: CLI Base

## Introdução

Este documento especifica os requisitos para a feature CLI Base do KiroSonar — uma CLI em Python que integra análise estática de código baseada em IA e refatoração automática diretamente no terminal. Esta feature estabelece o entry point da aplicação, o sistema de parsing de argumentos e o carregamento de regras de análise.

## Glossário

- **CLI**: Interface de Linha de Comando (Command Line Interface)
- **Entry_Point**: Função `main()` que serve como ponto de entrada da aplicação
- **Parser**: Componente `argparse` responsável por interpretar argumentos da linha de comando
- **Config_Loader**: Módulo `config.py` responsável por carregar regras de análise
- **DEFAULT_RULES**: Constante string contendo regras genéricas de fallback para análise de código
- **Subcomando**: Comando secundário do CLI (ex: `kirosonar analyze`)

## Requisitos

### Requisito 1: Instalação e Disponibilidade do Comando

**User Story:** Como desenvolvedor, quero instalar o KiroSonar via pip, para que o comando `kirosonar` fique disponível globalmente no meu terminal.

#### Critérios de Aceite

1. WHEN o desenvolvedor executa `pip install -e .` no diretório do projeto, THE Entry_Point SHALL registrar o comando `kirosonar` no PATH do sistema
2. WHEN a instalação é concluída com sucesso, THE CLI SHALL estar disponível para execução sem o prefixo `python`
3. IF a instalação falha por dependências ausentes, THEN THE Entry_Point SHALL exibir mensagem de erro descritiva e encerrar com código 1

### Requisito 2: Verificação de Versão do Python (Fail Fast)

**User Story:** Como desenvolvedor, quero que o KiroSonar valide a versão do Python no startup, para que eu receba feedback imediato se meu ambiente não for compatível.

#### Critérios de Aceite

1. WHEN o Entry_Point é iniciado com Python >= 3.11, THE CLI SHALL prosseguir com a execução normal
2. WHEN o Entry_Point é iniciado com Python < 3.11, THE CLI SHALL exibir a mensagem "Erro: KiroSonar requer Python 3.11 ou superior. Versão atual: {versão_atual}"
3. IF a versão do Python é inferior a 3.11, THEN THE Entry_Point SHALL encerrar a execução com código de saída 1
4. THE Entry_Point SHALL realizar a verificação de versão antes de qualquer outra operação

### Requisito 3: Exibição de Help do CLI

**User Story:** Como desenvolvedor, quero visualizar a ajuda do comando, para que eu entenda como usar o KiroSonar.

#### Critérios de Aceite

1. WHEN o desenvolvedor executa `kirosonar` sem argumentos, THE Parser SHALL exibir o menu de ajuda com os subcomandos disponíveis
2. WHEN o desenvolvedor executa `kirosonar --help`, THE Parser SHALL exibir descrição completa do CLI e suas opções
3. WHEN o desenvolvedor executa `kirosonar analyze --help`, THE Parser SHALL exibir descrição do subcomando analyze e suas flags

### Requisito 4: Subcomando Analyze com Flags Opcionais

**User Story:** Como desenvolvedor, quero executar análise de código via subcomando, para que eu possa especificar arquivos e regras customizadas.

#### Critérios de Aceite

1. THE Parser SHALL expor o subcomando `analyze` como comando principal de análise
2. WHEN o desenvolvedor executa `kirosonar analyze`, THE CLI SHALL executar o fluxo de análise usando git diff para detectar arquivos alterados
3. WHEN o desenvolvedor executa `kirosonar analyze --path <caminho>`, THE CLI SHALL analisar apenas o arquivo especificado, ignorando o git diff
4. WHEN o desenvolvedor executa `kirosonar analyze --rules <caminho>`, THE CLI SHALL carregar regras do arquivo especificado
5. WHEN ambas as flags `--path` e `--rules` são fornecidas, THE CLI SHALL usar o arquivo especificado em `--path` e as regras de `--rules`
6. IF o caminho fornecido em `--path` não existe, THEN THE CLI SHALL exibir mensagem de erro e encerrar com código 1

### Requisito 5: Orquestração do Fluxo Principal

**User Story:** Como desenvolvedor, quero que o CLI orquestre todas as etapas da análise, para que eu tenha uma experiência integrada no terminal.

#### Critérios de Aceite

1. WHEN o subcomando `analyze` é executado, THE Entry_Point SHALL chamar os módulos na seguinte ordem: git_module, config, prompt_builder, ai_service, report, autofix
2. THE Entry_Point SHALL montar um dicionário `args` com os argumentos parseados e passá-lo aos módulos consumidos
3. THE Entry_Point SHALL delegar toda lógica de negócio aos módulos específicos, mantendo apenas responsabilidade de orquestração
4. IF qualquer módulo consumido lançar exceção, THEN THE Entry_Point SHALL capturar a exceção, exibir mensagem amigável e encerrar com código 1

### Requisito 6: Carregamento de Regras de Análise

**User Story:** Como tech lead, quero definir regras customizadas de análise, para que a IA avalie o código com base nos padrões do meu time.

#### Critérios de Aceite

1. WHEN `load_rules()` é chamada sem argumentos e o arquivo `regras_empresa.md` existe no diretório atual, THE Config_Loader SHALL retornar o conteúdo do arquivo como string
2. WHEN `load_rules()` é chamada sem argumentos e o arquivo `regras_empresa.md` não existe, THE Config_Loader SHALL retornar o conteúdo de DEFAULT_RULES
3. WHEN `load_rules(rules_path)` é chamada com um caminho válido, THE Config_Loader SHALL retornar o conteúdo do arquivo especificado
4. IF `load_rules(rules_path)` é chamada com um caminho inválido, THEN THE Config_Loader SHALL retornar o conteúdo de DEFAULT_RULES
5. THE Config_Loader SHALL ler arquivos usando encoding UTF-8

### Requisito 7: Regras Padrão de Fallback

**User Story:** Como desenvolvedor, quero que existam regras padrão de análise, para que o KiroSonar funcione mesmo sem arquivo de regras customizado.

#### Critérios de Aceite

1. THE Config_Loader SHALL definir a constante DEFAULT_RULES contendo regras genéricas de boas práticas
2. THE DEFAULT_RULES SHALL incluir diretrizes sobre: princípios SOLID, convenções de nomenclatura, complexidade ciclomática, type hints, princípio DRY e docstrings
3. THE DEFAULT_RULES SHALL estar formatada em Markdown para consistência com regras customizadas

### Requisito 8: Conformidade com Padrões de Código

**User Story:** Como desenvolvedor, quero que o código do CLI siga padrões de qualidade, para que seja fácil de manter e estender.

#### Critérios de Aceite

1. THE Entry_Point SHALL seguir as convenções PEP 8 de estilo de código Python
2. THE Entry_Point SHALL incluir type hints em todas as funções e métodos
3. THE Entry_Point SHALL incluir docstrings descritivas em todas as funções públicas
4. THE Config_Loader SHALL seguir as convenções PEP 8 de estilo de código Python
5. THE Config_Loader SHALL incluir type hints em todas as funções e métodos
6. THE Config_Loader SHALL incluir docstrings descritivas em todas as funções públicas

### Requisito 9: Contratos de Interface

**User Story:** Como desenvolvedor do time, quero que os módulos exponham contratos claros, para que eu possa integrá-los e testá-los de forma independente.

#### Critérios de Aceite

1. THE Entry_Point SHALL expor a função `main() -> None` que lê argumentos de `sys.argv` e orquestra o fluxo
2. THE Config_Loader SHALL expor a função `load_rules(rules_path: str | None = None) -> str` que retorna o conteúdo das regras
3. FOR ALL chamadas válidas a `load_rules()`, THE Config_Loader SHALL retornar uma string não vazia
4. FOR ALL execuções do Entry_Point com argumentos válidos, THE CLI SHALL encerrar com código 0
