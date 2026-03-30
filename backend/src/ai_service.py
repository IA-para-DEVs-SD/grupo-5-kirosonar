"""LLM call service via kiro-cli subprocess.

Sends the assembled prompt to the LLM and returns the raw response.
Supports KIROSONAR_MOCK=1 for offline testing.
"""

import os
import re
import subprocess

# Regex que captura sequências de escape ANSI (cores, formatação, etc.)
_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")

MOCK_RESPONSE: str = """\
## Bugs
- Nenhum bug encontrado.

## Vulnerabilidades
- Nenhuma vulnerabilidade encontrada.

## Code Smells
- Variável com nome não descritivo (linha 10).

## Hotspots de Segurança
- Nenhum hotspot encontrado.

## Código Refatorado
[START]
def calcular_total(valor: float) -> float:
    return valor * 1.1
[END]
"""


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from a string.

    Args:
        text: Raw string potentially containing terminal color codes.

    Returns:
        Clean string without ANSI sequences.
    """
    return _ANSI_ESCAPE_RE.sub("", text)


def call_llm(prompt: str) -> str:
    """Send a prompt to the LLM via kiro-cli and return the response.

    Uses stdin (pipe) to avoid OS argument-length limits on large prompts.
    Strips ANSI escape codes from the output so reports are clean Markdown.

    Args:
        prompt: Complete prompt string to be sent.

    Returns:
        LLM response (stdout) without ANSI codes.

    Raises:
        RuntimeError: If the subprocess fails.
    """
    if os.environ.get("KIROSONAR_MOCK") == "1":
        return MOCK_RESPONSE

    # Envia o prompt via stdin para evitar limite de tamanho de argumento
    result = subprocess.run(
        ["kiro-cli", "chat", "--no-interactive", "--trust-tools="],
        input=prompt,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Erro ao chamar kiro-cli: {result.stderr}")
    return _strip_ansi(result.stdout.strip())
