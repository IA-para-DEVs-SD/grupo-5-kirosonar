"""LLM call service via kiro-cli subprocess.

Sends the assembled prompt to the LLM and returns the raw response.
Supports KIROSONAR_MOCK=1 for offline testing via mock_provider callable.
"""

import importlib
import os
import re
import subprocess
from typing import Callable

# Regex que captura sequências de escape ANSI (cores, formatação, etc.)
_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")

# Provider de mock injetável — carregado dinamicamente apenas quando KIROSONAR_MOCK=1
_mock_provider: Callable[[str], str] | None = None


def _get_mock_provider() -> Callable[[str], str]:
    """Carrega o mock provider dinamicamente na primeira chamada."""
    global _mock_provider
    if _mock_provider is None:
        module = importlib.import_module("tests.mock_responses")
        _mock_provider = module.get_mock_response
    return _mock_provider


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
        return _get_mock_provider()(prompt)

    try:
        result = subprocess.run(
            ["kiro-cli", "chat", "--no-interactive", "--trust-tools="],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("Timeout: kiro-cli não respondeu em 120 segundos.")

    if result.returncode != 0:
        raise RuntimeError(f"Erro ao chamar kiro-cli: {result.stderr}")
    return _strip_ansi(result.stdout.strip())
