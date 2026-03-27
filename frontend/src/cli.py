"""CLI entry point for KiroSonar.

Handles:
- Fail-fast Python version check (>= 3.11).
- Argument parsing via argparse ('analyze' subcommand).
- Orchestration of business-logic module calls.
"""

import argparse
import sys

from src.config import load_rules


# ---------------------------------------------------------------------------
# Verificação Fail-Fast de versão (executada no import do módulo)
# ---------------------------------------------------------------------------
if sys.version_info < (3, 11):
    print(
        f"Erro: KiroSonar requer Python >= 3.11. "
        f"Versão detectada: {sys.version_info.major}.{sys.version_info.minor}"
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Mocks temporários dos módulos ainda não implementados (TASK-02 a TASK-05)
# ---------------------------------------------------------------------------
def _mock_get_changed_files() -> list[str]:
    """Mock: simulates discovering changed files via git diff."""
    print("[mock] git_module.get_changed_files() -> ['src/exemplo.py']")
    return ["src/exemplo.py"]


def _mock_analyze_code(prompt: str) -> str:
    """Mock: simulates LLM response with a Markdown report."""
    print("[mock] ai_service.analyze_code() -> relatório fixo")
    return "## Relatório\n- Nenhum problema encontrado (mock)."


def _mock_save_report(content: str, path: str) -> None:
    """Mock: simulates saving the report to disk."""
    print(f"[mock] report.save_report() -> salvo em {path}")


def _mock_apply_fix(ai_response: str, file_path: str) -> None:
    """Mock: simulates applying the auto-fix."""
    print(f"[mock] autofix.apply_fix() -> fix aplicado em {file_path}")


# ---------------------------------------------------------------------------
# Construção do parser
# ---------------------------------------------------------------------------
def _build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI ArgumentParser.

    Returns:
        ArgumentParser configured with the 'analyze' subcommand.
    """
    parser = argparse.ArgumentParser(
        prog="kirosonar",
        description="KiroSonar — Code Review Inteligente e Auto-Fix via CLI.",
    )
    subparsers = parser.add_subparsers(dest="command")

    analyze = subparsers.add_parser(
        "analyze", help="Analisa arquivos alterados ou um arquivo específico."
    )
    analyze.add_argument(
        "--path",
        type=str,
        default=None,
        help="Caminho de um arquivo específico para análise (ignora git diff).",
    )
    analyze.add_argument(
        "--rules",
        type=str,
        default=None,
        help="Caminho para arquivo de regras customizado (.md).",
    )

    return parser


# ---------------------------------------------------------------------------
# Fluxo do subcomando analyze
# ---------------------------------------------------------------------------
def _run_analyze(args: argparse.Namespace) -> None:
    """Orchestrate the analysis flow by calling modules through their contracts.

    Args:
        args: argparse Namespace with --path and --rules flags.
    """
    rules = load_rules(args.rules)
    print(f"Regras carregadas ({len(rules)} caracteres).")

    # Descoberta de arquivos
    if args.path:
        files = [args.path]
    else:
        files = _mock_get_changed_files()

    # Análise e relatório por arquivo
    for file_path in files:
        print(f"\n📄 Analisando: {file_path}")
        prompt = f"Rules:\n{rules}\n\nFile: {file_path}"
        ai_response = _mock_analyze_code(prompt)
        _mock_save_report(ai_response, f"relatorios/{file_path}.md")
        _mock_apply_fix(ai_response, file_path)

    print("\n✅ Análise concluída.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    """Main entry point for the KiroSonar CLI."""
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "analyze":
        _run_analyze(args)
    else:
        parser.print_help()
