"""LLM call service via kiro-cli subprocess.

Sends the assembled prompt to the LLM and returns the raw response.
Supports KIROSONAR_MOCK=1 for offline testing via mock_provider callable.
"""

import importlib
import os
import re
import subprocess
import sys
import threading
import time
from typing import Callable

# Regex que captura sequências de escape ANSI (cores, formatação, etc.)
_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")

# Provider de mock injetável — carregado dinamicamente apenas quando KIROSONAR_MOCK=1
_mock_provider: Callable[[str], str] | None = None

# Timeout máximo em segundos
_TIMEOUT: int = 120

# Estimativa: ~0.3s por linha do prompt pra LLM processar
_SECONDS_PER_LINE: float = 0.3


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


def _show_progress(estimated: int, stop: threading.Event) -> None:
    """Exibe barra de progresso baseada em tempo estimado.

    Args:
        estimated: Tempo estimado em segundos.
        stop: Event que sinaliza fim do processo.
    """
    width = 30
    start = time.time()
    while not stop.is_set():
        elapsed = time.time() - start
        pct = min(elapsed / estimated, 0.95) if estimated > 0 else 0
        filled = int(width * pct)
        bar = "█" * filled + "░" * (width - filled)
        sys.stdout.write(f"\r  [{bar}] {elapsed:.0f}s / ~{estimated}s estimado")
        sys.stdout.flush()
        time.sleep(0.3)
    # Barra completa ao finalizar
    elapsed = time.time() - start
    bar = "█" * width
    sys.stdout.write(f"\r  [{bar}] {elapsed:.0f}s concluído.       \n")
    sys.stdout.flush()


def call_llm(prompt: str, show_progress: bool = True) -> str:
    """Send a prompt to the LLM via kiro-cli and return the response.

    Args:
        prompt: Complete prompt string to be sent.
        show_progress: Se True, exibe barra de progresso no terminal.

    Returns:
        LLM response (stdout) without ANSI codes.

    Raises:
        RuntimeError: If the subprocess fails.
    """
    if os.environ.get("KIROSONAR_MOCK") == "1":
        return _get_mock_provider()(prompt)

    # Estima tempo baseado no tamanho do prompt
    line_count = prompt.count("\n") + 1
    estimated = max(10, min(int(line_count * _SECONDS_PER_LINE), _TIMEOUT))

    stop = threading.Event()
    progress_thread = None
    if show_progress:
        progress_thread = threading.Thread(
            target=_show_progress, args=(estimated, stop), daemon=True
        )
        progress_thread.start()

    try:
        result = subprocess.run(
            ["kiro-cli", "chat", "--no-interactive", "--trust-tools="],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Timeout: kiro-cli não respondeu em {_TIMEOUT} segundos.")
    finally:
        stop.set()
        if progress_thread:
            progress_thread.join()

    if result.returncode != 0:
        raise RuntimeError(f"Erro ao chamar kiro-cli: {result.stderr}")
    return _strip_ansi(result.stdout.strip())
