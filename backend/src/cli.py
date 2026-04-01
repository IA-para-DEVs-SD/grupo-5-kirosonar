"""CLI entry point for KiroSonar.

Orchestrates the flow: file discovery → diff capture → LLM analysis → report → auto-fix.
"""

import argparse
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.ai_service import call_llm
from src.autofix import _validate_path, apply_fix
from src.chunker import split_into_chunks
from src.config import EXAMPLE_RULES_FILE, _discover_spec_files, load_rules
from src.git_module import get_changed_files, get_file_diff, read_file_content
from src.prompt_builder import build_prompt
from src.report import list_reports, save_report


def _check_python_version() -> None:
    """Terminate with error if Python < 3.11."""
    if sys.version_info < (3, 11):
        print("Erro: KiroSonar requer Python 3.11 ou superior.")
        sys.exit(1)


def _check_kiro_cli() -> None:
    """Verifica se kiro-cli está disponível no PATH. Ignora se KIROSONAR_MOCK=1."""
    if os.environ.get("KIROSONAR_MOCK") == "1":
        return
    if shutil.which("kiro-cli") is None:
        print("❌ kiro-cli não encontrado no PATH.")
        print("   Instale em: https://docs.aws.amazon.com/kiro/latest/userguide/kiro-cli.html")
        sys.exit(1)


def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser.

    Returns:
        ArgumentParser configured with subcommands.
    """
    parser = argparse.ArgumentParser(
        prog="kirosonar",
        description="Code Review Inteligente e Auto-Fix com IA.",
    )
    sub = parser.add_subparsers(dest="command")
    analyze = sub.add_parser("analyze", help="Analisa arquivos alterados ou específicos.")
    analyze.add_argument("--path", type=str, default=None, help="Arquivo específico para análise.")
    analyze.add_argument("--rules", type=str, default=None, help="Caminho para arquivo de regras.")
    sub.add_parser("report", help="Lista os relatórios gerados.")
    sub.add_parser("init", help="Cria regras_empresa.md a partir do template.")
    return parser


def _progress_bar(done: int, total: int, width: int = 25) -> str:
    """Retorna uma barra de progresso visual."""
    pct = done / total if total else 0
    filled = int(width * pct)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {done}/{total}"


def _analyze_chunk(chunk: str, rules: str, file_path: str, chunk_label: str) -> str | None:
    """Analisa um chunk individual via LLM."""
    prompt = build_prompt("", chunk, rules, f"{file_path} ({chunk_label})")
    try:
        return call_llm(prompt, show_progress=False)
    except RuntimeError:
        return None


def _analyze_file(
    file_path: str, rules: str, force_full: bool = False
) -> tuple[str, str | None, str | None, str]:
    """Analisa um único arquivo.

    Args:
        file_path: Caminho do arquivo a analisar.
        rules: Regras de análise carregadas.
        force_full: Se True, ignora diff e analisa arquivo completo.

    Returns:
        Tupla (file_path, response, error, diff).
    """
    try:
        _validate_path(file_path)
    except ValueError as exc:
        return file_path, None, str(exc), ""

    try:
        full_code = read_file_content(file_path)
    except FileNotFoundError:
        return file_path, None, f"Arquivo não encontrado: {file_path}", ""

    diff = "" if force_full else get_file_diff(file_path)

    # Com diff: análise normal
    if diff:
        prompt = build_prompt(diff, full_code, rules, file_path)
        try:
            response = call_llm(prompt)
        except RuntimeError as exc:
            return file_path, None, str(exc), diff
        return file_path, response, None, diff

    # Sem diff: tenta chunking pra arquivos grandes
    chunks = split_into_chunks(full_code, file_path)

    if len(chunks) == 1:
        prompt = build_prompt("", full_code, rules, file_path)
        try:
            response = call_llm(prompt)
        except RuntimeError as exc:
            return file_path, None, str(exc), ""
        return file_path, response, None, ""

    # Múltiplos chunks: analisa em paralelo
    total_c = len(chunks)
    print(f"   Arquivo grande — dividido em {total_c} trechos para análise.")
    print("   Aguarde, processando em paralelo...\n")

    responses: list[str] = []
    with ThreadPoolExecutor(max_workers=min(total_c, 4)) as pool:
        futures = {
            pool.submit(_analyze_chunk, chunk, rules, file_path, f"trecho {i + 1}"): i
            for i, chunk in enumerate(chunks)
        }
        done = 0
        for future in as_completed(futures):
            done += 1
            result = future.result()
            status = "✔" if result else "✘"
            print(f"   {_progress_bar(done, total_c)} {status}")
            if result:
                responses.append(result)

    if not responses:
        return file_path, None, "A IA não conseguiu analisar este arquivo.", ""

    combined = f"# Análise de {file_path}\n\n" + "\n\n---\n\n".join(responses)
    return file_path, combined, None, ""


def _cmd_report() -> None:
    """Exibe os relatórios existentes."""
    entries = list_reports()
    if not entries:
        print("Nenhum relatório encontrado.")
        return

    print(f"\n{'Arquivo':<50} {'Data':<20} {'Tamanho'}")
    print("-" * 80)
    for entry in entries:
        date_str = entry.generated_at.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{entry.name:<50} {date_str:<20} {entry.size_bytes} B")


def _cmd_init() -> None:
    """Cria regras_empresa.md a partir do template."""
    target = "regras_empresa.md"

    existing = _discover_spec_files()
    if existing:
        print("Regras de análise já detectadas no projeto:")
        for f in existing:
            print(f"  → {f}")
        print("O KiroSonar usará esses arquivos automaticamente.")
        return

    if os.path.isfile(target):
        print(f"'{target}' já existe.")
        return

    if not os.path.isfile(EXAMPLE_RULES_FILE):
        print("Template de regras não encontrado.")
        return

    shutil.copy2(EXAMPLE_RULES_FILE, target)
    print(f"✅ '{target}' criado com sucesso.")
    print("   Edite o arquivo com as convenções do seu time.")


def main() -> None:
    """Main entry point for the KiroSonar CLI."""
    _check_python_version()
    _check_kiro_cli()
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "report":
        _cmd_report()
        return

    if args.command == "init":
        _cmd_init()
        return

    if args.command != "analyze":
        parser.print_help()
        return

    rules = load_rules(args.rules)
    files = [args.path] if args.path else get_changed_files()

    if not files:
        print("Nenhum arquivo alterado encontrado.")
        return

    total = len(files)

    for idx, file_path in enumerate(files, 1):
        header = f"[{idx}/{total}] " if total > 1 else ""
        print(f"\n🔍 {header}{file_path}")

        file_path, response, error, diff = _analyze_file(
            file_path, rules, force_full=bool(args.path)
        )

        if error:
            print(f"   ❌ {error}")
            continue

        if not response:
            continue

        report_path = save_report(response, file_path)
        print(f"   📄 Relatório salvo: {report_path}")

        if diff and not args.path:
            print("   💡 Revise as sugestões no relatório e aplique manualmente.")
        else:
            apply_fix(response, file_path)

    print("\n✅ Análise finalizada.")
