# Documento de Requisitos

## Introdução

O módulo `report.py` é responsável por persistir o relatório gerado pela LLM como arquivo Markdown na pasta `relatorios/` do projeto analisado. Ele recebe o conteúdo textual da análise e o caminho do arquivo original analisado, gerando um nome de arquivo único com timestamp e salvando o conteúdo com encoding UTF-8. O módulo é independente dos demais módulos do KiroSonar e pode ser testado isoladamente com conteúdo mock.

## Glossário

- **Report_Module**: O módulo `src/report.py` responsável por persistir relatórios em Markdown.
- **Report_Name_Generator**: A função `generate_report_name()` que produz o nome do arquivo de relatório.
- **Report_Saver**: A função `save_report()` que orquestra a criação da pasta e a escrita do arquivo.
- **file_path**: Caminho do arquivo de código-fonte original que foi analisado pela LLM (ex: `src/app.py`).
- **safe_name**: Versão sanitizada do `file_path` com `/`, `\` e `.` substituídos por `_`.
- **timestamp**: String no formato `YYYYMMDD_HHMMSS` gerada no momento da chamada de `save_report()`.
- **relatorios/**: Diretório de destino dos relatórios, criado automaticamente na raiz do projeto em execução.
- **MOCK_CONTENT**: String Markdown fixa usada para testes independentes da LLM.

---

## Requisitos

### Requisito 1: Geração do Nome do Relatório

**User Story:** Como desenvolvedor, quero que o nome do arquivo de relatório seja único e identificável, para que eu consiga rastrear qual arquivo foi analisado e quando.

#### Critérios de Aceite

1. WHEN `generate_report_name(file_path)` é chamado com um `file_path` válido, THE `Report_Name_Generator` SHALL retornar uma string no formato `relatorios/<safe_name>_<timestamp>.md`.
2. WHEN `file_path` contém separadores `/` ou `\`, THE `Report_Name_Generator` SHALL substituir cada separador pelo caractere `_` no `safe_name`.
3. WHEN `file_path` contém o caractere `.`, THE `Report_Name_Generator` SHALL substituir cada `.` pelo caractere `_` no `safe_name`.
4. WHEN `generate_report_name(file_path)` é chamado, THE `Report_Name_Generator` SHALL incluir um `timestamp` no formato `YYYYMMDD_HHMMSS` no nome do arquivo gerado.
5. WHEN `generate_report_name(file_path)` é chamado duas vezes com o mesmo `file_path` em instantes distintos, THE `Report_Name_Generator` SHALL retornar nomes de arquivo diferentes.

---

### Requisito 2: Criação Automática do Diretório de Relatórios

**User Story:** Como desenvolvedor, quero que a pasta `relatorios/` seja criada automaticamente, para que eu não precise configurar o ambiente manualmente antes de executar a análise.

#### Critérios de Aceite

1. WHEN `save_report(content, file_path)` é chamado e o diretório `relatorios/` não existe, THE `Report_Saver` SHALL criar o diretório `relatorios/` antes de salvar o arquivo.
2. WHEN `save_report(content, file_path)` é chamado e o diretório `relatorios/` já existe, THE `Report_Saver` SHALL prosseguir com o salvamento sem lançar exceção.

---

### Requisito 3: Salvamento do Relatório em Markdown

**User Story:** Como desenvolvedor, quero que o relatório seja salvo como arquivo `.md` com encoding UTF-8, para que caracteres especiais do português sejam preservados corretamente.

#### Critérios de Aceite

1. WHEN `save_report(content, file_path)` é chamado com um `content` válido, THE `Report_Saver` SHALL criar um arquivo `.md` em `relatorios/` com o conteúdo exato recebido.
2. WHEN o arquivo de relatório é escrito, THE `Report_Saver` SHALL usar encoding `utf-8` na operação de escrita.
3. WHEN `save_report(content, file_path)` é chamado com `content` contendo caracteres especiais (acentos, cedilha), THE `Report_Saver` SHALL preservar esses caracteres no arquivo salvo.
4. WHEN `save_report(content, file_path)` é chamado com `MOCK_CONTENT` como `content`, THE `Report_Saver` SHALL salvar o arquivo sem depender de nenhum outro módulo do KiroSonar.

---

### Requisito 4: Retorno do Caminho Absoluto

**User Story:** Como desenvolvedor, quero que `save_report()` retorne o caminho absoluto do relatório salvo, para que o módulo orquestrador (`cli.py`) possa exibir ou referenciar o arquivo gerado.

#### Critérios de Aceite

1. WHEN `save_report(content, file_path)` é executado com sucesso, THE `Report_Saver` SHALL retornar o caminho absoluto do arquivo de relatório criado.
2. WHEN o caminho retornado por `save_report()` é verificado, THE `Report_Saver` SHALL retornar um caminho que aponta para um arquivo existente no sistema de arquivos.

---

### Requisito 5: Unicidade dos Relatórios

**User Story:** Como desenvolvedor, quero que relatórios de arquivos diferentes não colidam entre si, para que nenhum relatório seja sobrescrito acidentalmente.

#### Critérios de Aceite

1. WHEN `save_report()` é chamado com dois `file_path` distintos, THE `Report_Saver` SHALL gerar nomes de arquivo diferentes para cada relatório.
2. WHEN `save_report()` é chamado múltiplas vezes com o mesmo `file_path`, THE `Report_Saver` SHALL gerar nomes de arquivo distintos a cada chamada, garantidos pelo `timestamp`.

---

### Requisito 6: Feedback no Terminal

**User Story:** Como desenvolvedor, quero ver no terminal o caminho do relatório salvo, para que eu saiba onde encontrar o arquivo gerado após a análise.

#### Critérios de Aceite

1. WHEN `save_report(content, file_path)` é executado com sucesso, THE `Report_Saver` SHALL imprimir o caminho absoluto do relatório salvo na saída padrão (`stdout`).
