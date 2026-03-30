# Documento de Requisitos

## Introdução

O módulo `autofix.py` é responsável por extrair o código refatorado da resposta da LLM e aplicá-lo ao arquivo original com confirmação explícita do usuário. Ele recebe a resposta completa da IA como string Markdown, busca o conteúdo entre as tags `[START]` e `[END]` via Regex, exibe um preview no terminal e sobrescreve o arquivo somente após o usuário confirmar com `s` ou `S`. O módulo é independente dos demais módulos do KiroSonar e pode ser testado isoladamente com conteúdo mock.

## Glossário

- **AutoFix_Module**: O módulo `src/autofix.py` responsável por extrair e aplicar código refatorado.
- **Code_Extractor**: A função `extract_refactored_code()` que parseia a resposta da LLM.
- **Fix_Applier**: A função `apply_fix()` que orquestra o preview, a confirmação e a sobrescrita do arquivo.
- **ai_response**: String Markdown completa retornada pela LLM, podendo conter as tags `[START]` e `[END]`.
- **file_path**: Caminho do arquivo de código-fonte original a ser sobrescrito.
- **refactored_code**: Conteúdo extraído entre as tags `[START]` e `[END]` da resposta da LLM.
- **preview**: As primeiras 20 linhas do `refactored_code`, exibidas no terminal antes da confirmação.
- **MOCK_AI_RESPONSE**: String Markdown fixa usada para testes independentes da LLM.

---

## Requisitos

### Requisito 1: Extração do Código Refatorado

**User Story:** Como desenvolvedor, quero que o sistema extraia automaticamente o código refatorado da resposta da IA, para que eu não precise copiar e colar manualmente o código sugerido.

#### Critérios de Aceite

1. WHEN `extract_refactored_code(ai_response)` é chamado com uma string contendo `[START]` e `[END]`, THE `Code_Extractor` SHALL retornar o conteúdo entre as tags como string.
2. WHEN `extract_refactored_code(ai_response)` é chamado com uma string que não contém as tags `[START]` e `[END]`, THE `Code_Extractor` SHALL retornar `None`.
3. WHEN o conteúdo entre `[START]` e `[END]` contém múltiplas linhas, THE `Code_Extractor` SHALL capturar todas as linhas corretamente usando a flag `re.DOTALL`.
4. WHEN há espaços ou quebras de linha entre a tag `[START]` e o início do código, THE `Code_Extractor` SHALL ignorá-los e retornar apenas o código.
5. WHEN `extract_refactored_code(ai_response)` é chamado com `MOCK_AI_RESPONSE`, THE `Code_Extractor` SHALL retornar o código refatorado sem depender de nenhum outro módulo do KiroSonar.

---

### Requisito 2: Exibição do Preview no Terminal

**User Story:** Como desenvolvedor, quero visualizar um preview do código refatorado antes de decidir aplicá-lo, para que eu possa avaliar a qualidade da sugestão da IA.

#### Critérios de Aceite

1. WHEN `apply_fix(ai_response, file_path)` é chamado e há código refatorado, THE `Fix_Applier` SHALL exibir o caminho do arquivo que será alterado no terminal.
2. WHEN `apply_fix(ai_response, file_path)` é chamado e há código refatorado, THE `Fix_Applier` SHALL exibir no máximo as primeiras 20 linhas do código refatorado como preview.
3. WHEN o código refatorado tem menos de 20 linhas, THE `Fix_Applier` SHALL exibir todas as linhas disponíveis no preview.
4. WHEN `apply_fix(ai_response, file_path)` é chamado e não há código refatorado, THE `Fix_Applier` SHALL exibir uma mensagem informando que nenhum código refatorado foi encontrado.

---

### Requisito 3: Confirmação Interativa do Usuário

**User Story:** Como desenvolvedor, quero ser perguntado explicitamente antes de qualquer sobrescrita de arquivo, para que eu tenha controle total sobre quais alterações são aplicadas ao meu código.

#### Critérios de Aceite

1. WHEN há código refatorado disponível, THE `Fix_Applier` SHALL exibir o prompt `Deseja aplicar o fix em '<file_path>'? (s/n): ` antes de qualquer operação de escrita.
2. WHEN o usuário digita `s`, THE `Fix_Applier` SHALL prosseguir com a sobrescrita do arquivo.
3. WHEN o usuário digita `S`, THE `Fix_Applier` SHALL prosseguir com a sobrescrita do arquivo.
4. WHEN o usuário digita qualquer entrada diferente de `s` ou `S`, THE `Fix_Applier` SHALL não sobrescrever o arquivo.
5. WHEN não há código refatorado, THE `Fix_Applier` SHALL retornar `False` sem exibir o prompt de confirmação.

---

### Requisito 4: Sobrescrita do Arquivo com Encoding UTF-8

**User Story:** Como desenvolvedor, quero que o arquivo seja sobrescrito com o código refatorado usando encoding UTF-8, para que caracteres especiais do português sejam preservados corretamente.

#### Critérios de Aceite

1. WHEN o usuário confirma com `s` ou `S`, THE `Fix_Applier` SHALL sobrescrever o arquivo em `file_path` com o `refactored_code` extraído.
2. WHEN o arquivo é sobrescrito, THE `Fix_Applier` SHALL usar encoding `utf-8` na operação de escrita.
3. WHEN o arquivo é sobrescrito com sucesso, THE `Fix_Applier` SHALL exibir uma mensagem de confirmação no terminal.
4. WHEN o arquivo é sobrescrito com sucesso, THE `Fix_Applier` SHALL retornar `True`.

---

### Requisito 5: Retorno de Status da Operação

**User Story:** Como desenvolvedor, quero que `apply_fix()` retorne um booleano indicando se o fix foi aplicado, para que o orquestrador (`cli.py`) possa registrar o resultado da operação.

#### Critérios de Aceite

1. WHEN `apply_fix()` sobrescreve o arquivo com sucesso, THE `Fix_Applier` SHALL retornar `True`.
2. WHEN o usuário recusa a aplicação digitando qualquer entrada diferente de `s`/`S`, THE `Fix_Applier` SHALL retornar `False`.
3. WHEN não há código refatorado na resposta da IA, THE `Fix_Applier` SHALL retornar `False`.

---

### Requisito 6: Independência de Módulos

**User Story:** Como desenvolvedor, quero que o módulo `autofix.py` funcione de forma independente, para que eu possa testá-lo e depurá-lo sem precisar dos demais módulos do KiroSonar.

#### Critérios de Aceite

1. WHEN `autofix.py` é executado com `MOCK_AI_RESPONSE`, THE `AutoFix_Module` SHALL funcionar corretamente sem importar nenhum outro módulo interno do KiroSonar.
2. WHEN `autofix.py` é importado, THE `AutoFix_Module` SHALL depender apenas da Standard Library Python (`re`, `os`).
