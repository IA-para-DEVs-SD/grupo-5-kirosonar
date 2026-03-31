"""Prompt assembly for LLM submission.

Builds a structured prompt with explicit weighting between the diff
(maximum priority) and the full file content (medium priority),
as specified in RF-01 of the PRD.
"""


def _sanitize_user_content(text: str) -> str:
    """Sanitiza conteúdo do usuário para prevenir prompt injection.

    Delimita claramente dados do usuário vs instruções do sistema,
    removendo padrões que poderiam ser interpretados como instruções.
    """
    # Remove padrões comuns de prompt injection (case-insensitive)
    sanitized = text.replace("```", "` ` `")
    text_lower = sanitized.lower()
    for marker in ["[system]", "[inst]", "<<sys>>", "<</sys>>", "[/inst]"]:
        idx = text_lower.find(marker)
        while idx != -1:
            sanitized = sanitized[:idx] + sanitized[idx + len(marker) :]
            text_lower = sanitized.lower()
            idx = text_lower.find(marker)
    return sanitized


def build_prompt(diff: str, full_code: str, rules: str, file_path: str) -> str:
    """Assemble the complete prompt for the LLM.

    Args:
        diff: Git diff output for the file (may be empty when using --path).
        full_code: Full content of the file under analysis.
        rules: Company rules string.
        file_path: File name/path for context.

    Returns:
        Formatted prompt instructing the LLM to return the report
        in the fixed template with refactored code between [START]/[END].
    """
    # Sanitiza conteúdo do usuário antes de injetar no prompt
    full_code = _sanitize_user_content(full_code)
    diff = _sanitize_user_content(diff) if diff else diff

    # Seção de diff só é incluída quando há alterações
    diff_section = ""
    if diff:
        diff_section = (
            "## Diff das Alterações (PESO MÁXIMO — foco principal da análise)\n"
            f"```diff\n{diff}\n```\n\n"
        )

    return (
        f"Você é um auditor de código sênior. Analise o arquivo '{file_path}' "
        f"com base nas regras abaixo e retorne EXATAMENTE no template indicado.\n\n"
        f"## Regras da Empresa\n{rules}\n\n"
        f"{diff_section}"
        f"## Arquivo Completo (PESO MÉDIO — contexto para entender o impacto)\n"
        f"```\n{full_code}\n```\n\n"
        f"## Template de Resposta (siga exatamente)\n"
        f"## Bugs\n(lista)\n\n"
        f"## Vulnerabilidades\n(lista)\n\n"
        f"## Code Smells\n(lista)\n\n"
        f"## Hotspots de Segurança\n(lista)\n\n"
        f"## Código Refatorado\n[START]\n(código refatorado completo)\n[END]"
    )
