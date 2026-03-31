"""Extração e aplicação do código refatorado (Auto-Fix)."""

import os
import re
import shutil

from src.git_module import get_repo_root


def _validate_path(file_path: str) -> None:
    """Valida que file_path está dentro do repositório Git (previne path traversal).

    Raises:
        ValueError: Se o caminho está fora do repositório.
    """
    repo_root = os.path.realpath(get_repo_root())
    resolved = os.path.realpath(file_path)
    if not resolved.startswith(repo_root + os.sep) and resolved != repo_root:
        raise ValueError(f"Caminho fora do repositório: {file_path}")


def extract_refactored_code(ai_response: str) -> str | None:
    """Extrai o código refatorado da resposta da LLM.

    Args:
        ai_response: String Markdown completa retornada pela LLM.

    Returns:
        Código refatorado ou None se as tags não forem encontradas.
    """
    match = re.search(r"\[START\]\s*\n(.*?)\n\s*\[END\]", ai_response, re.DOTALL)
    return match.group(1) if match else None


def apply_fix(ai_response: str, file_path: str) -> bool:
    """Aplica o código refatorado ao arquivo original.

    Args:
        ai_response: String Markdown completa retornada pela LLM.
        file_path: Caminho do arquivo original a ser sobrescrito.

    Returns:
        True se o fix foi aplicado, False caso contrário.
    """
    code = extract_refactored_code(ai_response)
    if code is None:
        print("⚠️  Nenhum código refatorado encontrado na resposta da IA.")
        return False

    _validate_path(file_path)

    preview = "\n".join(code.splitlines()[:20])
    print(f"\n📝 Preview do código refatorado para '{file_path}':\n{preview}\n")

    answer = input(f"Deseja aplicar o fix em '{file_path}'? (s/n): ").strip().lower()
    if answer != "s":
        print("❌ Fix não aplicado.")
        return False

    backup_path = file_path + ".bak"
    shutil.copy2(file_path, backup_path)
    print(f"💾 Backup salvo em '{backup_path}'.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"✅ Fix aplicado em '{file_path}'.")
    return True
