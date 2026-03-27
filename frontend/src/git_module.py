"""Git infrastructure module for KiroSonar.

Responsible for interacting with Git via subprocess to discover
changed files in the working tree and read their contents.
"""

import subprocess
import sys


def get_changed_files() -> list[str]:
    """Execute 'git diff --name-only' and return the list of changed files.

    Returns:
        List of relative paths of modified files.
        Returns an empty list if there are no changes.

    Raises:
        SystemExit: If the current directory is not a valid Git repository.
    """
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        capture_output=True,
        text=True,
    )

    # returncode != 0 indica que não é um repositório Git válido
    if result.returncode != 0:
        print(
            "Erro: o diretório atual não é um repositório Git válido.\n"
            f"Detalhes: {result.stderr.strip()}"
        )
        sys.exit(1)

    # Filtra linhas vazias geradas pelo split do output
    changed_files = [line for line in result.stdout.splitlines() if line.strip()]

    return changed_files


def read_file_content(file_path: str) -> str:
    """Read and return the full content of a file.

    Args:
        file_path: Relative or absolute path to the file.

    Returns:
        File content as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
