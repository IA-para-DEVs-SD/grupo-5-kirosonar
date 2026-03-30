"""Git integration module via subprocess.

Provides functions to discover changed files, retrieve per-file diffs,
and read full file contents from the working tree.
"""

import subprocess
import sys


def get_changed_files() -> list[str]:
    """Execute 'git diff --name-only' and return the list of changed files.

    Returns:
        List of relative paths of modified files.

    Raises:
        SystemExit: If the current directory is not a valid Git repository.
    """
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("Erro: o diretório atual não é um repositório Git válido.")
        sys.exit(1)
    return [line for line in result.stdout.strip().splitlines() if line]


def get_file_diff(file_path: str) -> str:
    """Execute 'git diff <file>' and return the diff output for a single file.

    Args:
        file_path: Relative path of the file to diff.

    Returns:
        Diff string. Empty string when there are no unstaged changes.
    """
    result = subprocess.run(
        ["git", "diff", file_path],
        capture_output=True,
        text=True,
    )
    # Se falhar (ex: arquivo não rastreado), retorna vazio em vez de quebrar
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def read_file_content(file_path: str) -> str:
    """Read and return the full content of a file.

    Args:
        file_path: Relative or absolute path to the file.

    Returns:
        File content as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    with open(file_path, encoding="utf-8") as f:
        return f.read()
