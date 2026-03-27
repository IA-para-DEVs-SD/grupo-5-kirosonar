# US-02: Aplicação interativa de Auto-Fix sugerido pela IA

## Descrição

> **Como** desenvolvedor que recebeu sugestões de refatoração da IA,
> **eu quero** visualizar um preview do código refatorado e decidir se aplico ou não a correção
> **para que** eu mantenha controle total sobre as alterações no meu código, evitando sobrescritas indesejadas.

## Contexto

O Auto-Fix é o diferencial competitivo do KiroSonar em relação a ferramentas tradicionais como o SonarQube. Porém, como a IA pode alucinar, a aprovação humana explícita (s/n) é obrigatória antes de qualquer sobrescrita. Isso mitiga o risco de alterações indesejadas no código de produção.

## Critérios de Aceite

- [ ] Após a análise, se a resposta da IA contiver código refatorado entre as tags `[START]` e `[END]`, o sistema exibe um preview das primeiras 20 linhas no terminal.
- [ ] O sistema pergunta interativamente: "Deseja aplicar o fix em '<arquivo>'? (s/n)".
- [ ] Se o usuário digitar `s` ou `S`, o arquivo original é sobrescrito com o código refatorado (encoding UTF-8).
- [ ] Se o usuário digitar qualquer outra coisa, o fix não é aplicado e o sistema informa "Fix não aplicado."
- [ ] Se a resposta da IA não contiver as tags `[START]`/`[END]`, o sistema informa que não há código refatorado e segue sem erro.
- [ ] O arquivo original só é alterado após confirmação explícita — nunca automaticamente.

## Módulos Envolvidos

| Módulo | Responsabilidade |
|---|---|
| `src/autofix.py` | Extração do código refatorado e aplicação com confirmação |
| `src/cli.py` | Chamada ao `apply_fix()` após receber a resposta da LLM |

## Fluxo

```
resposta da LLM recebida
    → extract_refactored_code(ai_response)
        → regex: [START]...[END]
    → se encontrou código:
        → exibe preview (20 linhas)
        → prompt: "Deseja aplicar o fix? (s/n)"
        → se 's': sobrescreve arquivo
        → se 'n': informa e segue
    → se não encontrou:
        → informa e segue
```

## Notas Técnicas

- Regex utilizado: `r'\[START\]\s*\n(.*?)\n\s*\[END\]'` com flag `re.DOTALL`.
- O preview é limitado a 20 linhas para não poluir o terminal em arquivos grandes.
- Não há mecanismo de rollback no MVP. O desenvolvedor deve usar `git checkout` para reverter se necessário.
