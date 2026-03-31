"""Testes de integração do KiroSonar com projetos JavaScript."""

import os
import subprocess
from pathlib import Path

JS_PROJECT_PATH = Path(__file__).parent / "js-project" / "src"
BACKEND_PATH = Path(__file__).parent.parent
REPORTS_PATH = BACKEND_PATH / "relatorios"


def run_kirosonar_analyze(file_path: str) -> tuple[str, int]:
    """Executa kirosonar analyze em um arquivo e retorna o conteúdo do relatório.

    Args:
        file_path: Caminho do arquivo a analisar.

    Returns:
        Tuple de (report_content, return_code).
    """
    # Limpa relatórios antigos
    if REPORTS_PATH.exists():
        for old_report in REPORTS_PATH.glob("*.md"):
            old_report.unlink()

    # Usa o comando kirosonar do venv
    kirosonar_cmd = BACKEND_PATH / ".venv" / "bin" / "kirosonar"

    # Garante que ~/.local/bin está no PATH (onde kiro-cli está instalado)
    env = os.environ.copy()
    local_bin = Path.home() / ".local" / "bin"
    env["PATH"] = f"{local_bin}:{env.get('PATH', '')}"

    result = subprocess.run(
        [str(kirosonar_cmd), "analyze", "--path", file_path],
        capture_output=True,
        text=True,
        cwd=BACKEND_PATH,
        env=env,
        input="n\n",  # Responde "n" para o prompt de autofix
    )

    # Lê o relatório gerado
    report_content = ""
    if REPORTS_PATH.exists():
        reports = list(REPORTS_PATH.glob("*.md"))
        if reports:
            # Pega o relatório mais recente
            latest_report = max(reports, key=lambda p: p.stat().st_mtime)
            report_content = latest_report.read_text(encoding="utf-8")

    return report_content, result.returncode


class TestDetection:
    """Integration tests for error detection."""

    def test_detects_unused_variables(self):
        """Test kirosonar analyze detects unused variables."""
        file_path = JS_PROJECT_PATH / "unused_vars.js"
        output, _ = run_kirosonar_analyze(str(file_path))

        assert any(
            term in output.lower() for term in ["unused", "não utilizada", "nunca utilizada"]
        ), f"Expected unused variable detection in output: {output}"

    def test_detects_unreachable_code(self):
        """Test kirosonar analyze detects unreachable code."""
        file_path = JS_PROJECT_PATH / "unreachable_code.js"
        output, _ = run_kirosonar_analyze(str(file_path))

        assert any(
            term in output.lower() for term in ["unreachable", "inalcançável", "dead code"]
        ), f"Expected unreachable code detection in output: {output}"

    def test_detects_duplicate_code(self):
        """Test kirosonar analyze detects duplicate code."""
        file_path = JS_PROJECT_PATH / "duplicate_code.js"
        output, _ = run_kirosonar_analyze(str(file_path))

        assert any(term in output.lower() for term in ["duplicate", "duplicado", "repetido"]), (
            f"Expected duplicate code detection in output: {output}"
        )

    def test_detects_security_vulnerability(self):
        """Test kirosonar analyze detects eval() usage."""
        file_path = JS_PROJECT_PATH / "security_issues.js"
        output, _ = run_kirosonar_analyze(str(file_path))

        assert any(
            term in output.lower() for term in ["eval", "security", "segurança", "vulnerab"]
        ), f"Expected security vulnerability detection in output: {output}"

    def test_detects_long_function(self):
        """Test kirosonar analyze detects long functions."""
        file_path = JS_PROJECT_PATH / "code_smells.js"
        output, _ = run_kirosonar_analyze(str(file_path))

        assert any(
            term in output.lower() for term in ["long", "longa", "complexa", "lines", "linhas"]
        ), f"Expected long function detection in output: {output}"

    def test_detects_loose_equality(self):
        """Test kirosonar analyze detects == instead of ===."""
        file_path = JS_PROJECT_PATH / "comparisons.js"
        output, _ = run_kirosonar_analyze(str(file_path))

        assert any(
            term in output.lower() for term in ["===", "strict", "equality", "igualdade"]
        ), f"Expected loose equality detection in output: {output}"

    def test_detects_console_log(self):
        """Test kirosonar analyze detects console.log."""
        file_path = JS_PROJECT_PATH / "console_logs.js"
        output, _ = run_kirosonar_analyze(str(file_path))

        assert any(term in output.lower() for term in ["console", "log", "debug"]), (
            f"Expected console.log detection in output: {output}"
        )

    def test_detects_implicit_global(self):
        """Test kirosonar analyze detects implicit global variables."""
        file_path = JS_PROJECT_PATH / "global_vars.js"
        output, _ = run_kirosonar_analyze(str(file_path))

        assert any(
            term in output.lower() for term in ["global", "let", "const", "var", "declaração"]
        ), f"Expected implicit global detection in output: {output}"

    def test_detects_callback_hell(self):
        """Test kirosonar analyze detects deeply nested callbacks."""
        file_path = JS_PROJECT_PATH / "callback_hell.js"
        output, _ = run_kirosonar_analyze(str(file_path))

        assert any(
            term in output.lower()
            for term in ["callback", "nested", "aninhado", "async", "promise"]
        ), f"Expected callback hell detection in output: {output}"

    def test_detects_missing_error_handling(self):
        """Test kirosonar analyze detects missing catch block."""
        file_path = JS_PROJECT_PATH / "error_handling.js"
        output, _ = run_kirosonar_analyze(str(file_path))

        assert any(
            term in output.lower() for term in ["catch", "error", "erro", "exception", "try"]
        ), f"Expected missing error handling detection in output: {output}"
