"""CLI entry point for KiroSonar.

Orchestrates the flow: file discovery → diff capture → LLM analysis → report → auto-fix.
"""

import argparse
import sys

from dotenv import load_dotenv
load_dotenv()

from src.ai_service import call_llm
from src.autofix import apply_fix
from src.config import load_rules
from src.git_module import get_changed_files, get_file_diff, read_file_content
from src.prompt_builder import build_prompt
from src.report import save_report, list_reports


def _check_python_version() -> None:
    """Terminate with error if Python < 3.11."""
    if sys.version_info < (3, 11):
        print("Erro: KiroSonar requer Python 3.11 ou superior.")
        sys.exit(1)


def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser.

    Returns:
        ArgumentParser configured with the 'analyze' subcommand.
    """
    parser = argparse.ArgumentParser(
        prog="kirosonar",
        description="Code Review Inteligente e Auto-Fix com IA.",
    )
    sub = parser.add_subparsers(dest="command")
    analyze = sub.add_parser("analyze", help="Analisa arquivos alterados ou específicos.")
    analyze.add_argument("--path", type=str, default=None, help="Arquivo específico para análise.")
    analyze.add_argument("--rules", type=str, default=None, help="Caminho para arquivo de regras.")
    sub.add_parser("report", help="Lista os relatórios gerados em relatorios/.")
    return parser


def _cmd_report() -> None:
    """Exibe os relatórios existentes em relatorios/, ordenados por data."""
    entries = list_reports()
    if not entries:
        print("Nenhum relatório encontrado.")
        return

    print(f"{'Arquivo':<50} {'Data de Geração':<20} {'Tamanho'}")
    print("-" * 80)
    for entry in entries:
        date_str = entry.generated_at.strftime("%Y-%m-%d %H:%M:%S")
        size_str = f"{entry.size_bytes} B"
        print(f"{entry.name:<50} {date_str:<20} {size_str}")


def main() -> None:
    """Main entry point for the KiroSonar CLI."""
    _check_python_version()
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "report":
        _cmd_report()
        return

    if args.command != "analyze":
        parser.print_help()
        return

    rules = load_rules(args.rules)
    files = [args.path] if args.path else get_changed_files()

    if not files:
        print("Nenhum arquivo alterado encontrado.")
        return

    for file_path in files:
        print(f"\n🔍 Analisando: {file_path}")

        try:
            full_code = read_file_content(file_path)
        except FileNotFoundError:
            print(f"⚠️  Arquivo não encontrado: {file_path}")
            continue

        # Diff só é capturado no fluxo git (sem --path)
        diff = "" if args.path else get_file_diff(file_path)

        prompt = build_prompt(diff, full_code, rules, file_path)

        try:
            response = call_llm(prompt)
        except RuntimeError as exc:
            print(f"❌ Erro na análise de '{file_path}': {exc}")
            continue

        report_path = save_report(response, file_path)
        print(f"📄 Relatório salvo em: {report_path}")
        apply_fix(response, file_path)
