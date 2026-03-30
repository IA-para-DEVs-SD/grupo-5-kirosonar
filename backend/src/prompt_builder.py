"""Prompt assembly for LLM submission.

Builds a structured prompt with explicit weighting between the diff
(maximum priority) and the full file content (medium priority),
as specified in RF-01 of the PRD.
"""


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
