"""Unit tests for src.cli module."""

import sys
from unittest.mock import patch

import pytest

from src.cli import _build_parser, main


class TestBuildParser:
    """Tests for the _build_parser function."""

    def test_parser_has_analyze_subcommand(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["analyze"])
        assert args.command == "analyze"

    def test_analyze_path_defaults_to_none(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["analyze"])
        assert args.path is None

    def test_analyze_rules_defaults_to_none(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["analyze"])
        assert args.rules is None

    def test_analyze_accepts_path_flag(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["analyze", "--path", "src/app.py"])
        assert args.path == "src/app.py"

    def test_analyze_accepts_rules_flag(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["analyze", "--rules", "rules.md"])
        assert args.rules == "rules.md"


class TestMain:
    """Tests for the main entry point."""

    @patch("src.cli._check_kiro_cli")
    def test_no_command_prints_help(self, mock_check, capsys) -> None:
        with patch("sys.argv", ["kirosonar"]):
            main()
        output = capsys.readouterr().out
        assert "usage:" in output.lower()

    @patch("src.cli._check_kiro_cli")
    @patch("src.cli.apply_fix")
    @patch("src.cli.save_report", return_value="/tmp/report.md")
    @patch("src.cli.call_llm", return_value="## Bugs\n- Nenhum")
    @patch("src.cli.read_file_content", return_value="print('hello')")
    def test_analyze_with_path_runs_full_flow(
        self, mock_read, mock_llm, mock_report, mock_fix, mock_check, capsys
    ) -> None:
        """--path should skip git diff and run the full pipeline."""
        with patch("sys.argv", ["kirosonar", "analyze", "--path", "file.py"]):
            main()
        output = capsys.readouterr().out
        assert "file.py" in output
        mock_read.assert_called_once_with("file.py")
        mock_llm.assert_called_once()
        mock_report.assert_called_once()
        mock_fix.assert_called_once()

    @patch("src.cli._check_kiro_cli")
    @patch("src.cli.apply_fix")
    @patch("src.cli.save_report", return_value="/tmp/report.md")
    @patch("src.cli.call_llm", return_value="## Bugs\n- Nenhum")
    @patch("src.cli.read_file_content", return_value="print('hello')")
    @patch("src.cli.get_file_diff", return_value="@@ -1 +1 @@\n-old\n+new")
    @patch("src.cli.get_changed_files", return_value=["src/app.py"])
    def test_analyze_git_flow_includes_diff(
        self, mock_files, mock_diff, mock_read, mock_llm, mock_report, mock_fix, mock_check, capsys
    ) -> None:
        """Without --path, should call get_file_diff for each changed file."""
        with patch("sys.argv", ["kirosonar", "analyze"]):
            main()
        mock_diff.assert_called_once_with("src/app.py")
        mock_llm.assert_called_once()

    @patch("src.cli._check_kiro_cli")
    @patch("src.cli.get_changed_files", return_value=[])
    def test_analyze_no_files_prints_message(self, mock_git, mock_check, capsys) -> None:
        with patch("sys.argv", ["kirosonar", "analyze"]):
            main()
        output = capsys.readouterr().out
        assert "Nenhum arquivo alterado encontrado" in output

    @patch("src.cli._check_kiro_cli")
    @patch("src.cli.read_file_content", side_effect=FileNotFoundError)
    def test_analyze_missing_file_skips_gracefully(self, mock_read, mock_check, capsys) -> None:
        """--path with non-existent file should print warning and continue."""
        with patch("sys.argv", ["kirosonar", "analyze", "--path", "ghost.py"]):
            main()
        output = capsys.readouterr().out
        assert "Arquivo não encontrado" in output

    def test_check_python_version_exits_on_old_python(self) -> None:
        with patch("src.cli.sys") as mock_sys:
            mock_sys.version_info = (3, 10)
            mock_sys.exit = sys.exit
            with pytest.raises(SystemExit):
                from src.cli import _check_python_version

                _check_python_version()

    @patch("src.cli._check_kiro_cli")
    @patch("src.cli._validate_path", side_effect=ValueError("Caminho fora do repositório"))
    def test_analyze_path_traversal_skips(self, mock_val, mock_check, capsys) -> None:
        with patch("sys.argv", ["kirosonar", "analyze", "--path", "/etc/passwd"]):
            main()
        output = capsys.readouterr().out
        assert "Caminho fora do repositório" in output

    @patch("src.cli._check_kiro_cli")
    @patch("src.cli.read_file_content", return_value="code")
    @patch("src.cli.call_llm", side_effect=RuntimeError("Timeout"))
    def test_analyze_llm_error_skips(self, mock_llm, mock_read, mock_check, capsys) -> None:
        with patch("sys.argv", ["kirosonar", "analyze", "--path", "file.py"]):
            main()
        output = capsys.readouterr().out
        assert "Timeout" in output


class TestReportCommand:
    """Tests for the 'report' subcommand."""

    @patch("src.cli._check_kiro_cli")
    @patch("src.cli.list_reports", return_value=[])
    def test_report_empty_prints_no_reports(self, mock_list, mock_check, capsys) -> None:
        with patch("sys.argv", ["kirosonar", "report"]):
            main()
        output = capsys.readouterr().out
        assert "Nenhum relatório encontrado." in output

    @patch("src.cli._check_kiro_cli")
    @patch("src.cli.list_reports")
    def test_report_lists_entries(self, mock_list, mock_check, capsys) -> None:
        from datetime import datetime

        from src.report import ReportEntry

        mock_list.return_value = [
            ReportEntry(
                name="src_app_py_20260318_173000.md",
                generated_at=datetime(2026, 3, 18, 17, 30, 0),
                size_bytes=1024,
            )
        ]
        with patch("sys.argv", ["kirosonar", "report"]):
            main()
        output = capsys.readouterr().out
        assert "src_app_py_20260318_173000.md" in output
        assert "2026-03-18 17:30:00" in output
        assert "1024 B" in output

    def test_report_subcommand_registered_in_parser(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["report"])
        assert args.command == "report"


class TestCheckKiroCli:
    """Tests for _check_kiro_cli."""

    @patch.dict("os.environ", {"KIROSONAR_MOCK": "1"})
    def test_skips_check_when_mock_enabled(self) -> None:
        from src.cli import _check_kiro_cli

        # Should not raise
        _check_kiro_cli()

    @patch.dict("os.environ", {"KIROSONAR_MOCK": "0"})
    @patch("src.cli.shutil.which", return_value="/usr/bin/kiro-cli")
    def test_passes_when_kiro_cli_found(self, mock_which) -> None:
        from src.cli import _check_kiro_cli

        _check_kiro_cli()

    @patch.dict("os.environ", {"KIROSONAR_MOCK": "0"})
    @patch("src.cli.shutil.which", return_value=None)
    def test_exits_when_kiro_cli_not_found(self, mock_which) -> None:
        from src.cli import _check_kiro_cli

        with pytest.raises(SystemExit):
            _check_kiro_cli()


class TestProgressBar:
    """Tests for _progress_bar."""

    def test_returns_string(self) -> None:
        from src.cli import _progress_bar

        result = _progress_bar(5, 10)
        assert isinstance(result, str)

    def test_shows_done_and_total(self) -> None:
        from src.cli import _progress_bar

        result = _progress_bar(3, 7)
        assert "3/7" in result

    def test_zero_total_does_not_crash(self) -> None:
        from src.cli import _progress_bar

        result = _progress_bar(0, 0)
        assert "0/0" in result


class TestCmdInit:
    """Tests for the 'init' subcommand."""

    @patch("src.cli._check_kiro_cli")
    @patch("src.cli._discover_spec_files", return_value=["regras_empresa.md"])
    def test_init_with_existing_specs_prints_message(self, mock_specs, mock_check, capsys) -> None:
        with patch("sys.argv", ["kirosonar", "init"]):
            main()
        output = capsys.readouterr().out
        assert "Regras de análise já detectadas" in output

    @patch("src.cli._check_kiro_cli")
    @patch("src.cli._discover_spec_files", return_value=[])
    @patch("src.cli.os.path.isfile")
    def test_init_when_target_already_exists(
        self, mock_isfile, mock_specs, mock_check, capsys
    ) -> None:
        mock_isfile.return_value = True
        with patch("sys.argv", ["kirosonar", "init"]):
            main()
        output = capsys.readouterr().out
        assert "já existe" in output

    @patch("src.cli._check_kiro_cli")
    @patch("src.cli._discover_spec_files", return_value=[])
    @patch("src.cli.os.path.isfile", return_value=False)
    def test_init_when_template_not_found(
        self, mock_isfile, mock_specs, mock_check, capsys
    ) -> None:
        with patch("sys.argv", ["kirosonar", "init"]):
            main()
        output = capsys.readouterr().out
        assert "Template de regras não encontrado" in output


class TestAnalyzeFile:
    """Tests for _analyze_file."""

    @patch("src.cli._validate_path", side_effect=ValueError("fora do repo"))
    def test_returns_error_on_invalid_path(self, mock_val) -> None:
        from src.cli import _analyze_file

        path, response, error, diff = _analyze_file("/etc/passwd", "rules")
        assert error == "fora do repo"
        assert response is None

    @patch("src.cli._validate_path")
    @patch("src.cli.read_file_content", side_effect=FileNotFoundError)
    def test_returns_error_on_missing_file(self, mock_read, mock_val) -> None:
        from src.cli import _analyze_file

        path, response, error, diff = _analyze_file("ghost.py", "rules")
        assert "Arquivo não encontrado" in error

    @patch("src.cli._validate_path")
    @patch("src.cli.read_file_content", return_value="print('hi')")
    @patch("src.cli.get_file_diff", return_value="@@ diff @@")
    @patch("src.cli.call_llm", return_value="review result")
    def test_returns_response_with_diff(self, mock_llm, mock_diff, mock_read, mock_val) -> None:
        from src.cli import _analyze_file

        path, response, error, diff = _analyze_file("file.py", "rules")
        assert response == "review result"
        assert error is None

    @patch("src.cli._validate_path")
    @patch("src.cli.read_file_content", return_value="print('hi')")
    @patch("src.cli.get_file_diff", return_value="@@ diff @@")
    @patch("src.cli.call_llm", side_effect=RuntimeError("timeout"))
    def test_returns_error_on_llm_failure_with_diff(
        self, mock_llm, mock_diff, mock_read, mock_val
    ) -> None:
        from src.cli import _analyze_file

        path, response, error, diff = _analyze_file("file.py", "rules")
        assert "timeout" in error
        assert response is None

    @patch("src.cli._validate_path")
    @patch("src.cli.read_file_content", return_value="x = 1\n")
    @patch("src.cli.get_file_diff", return_value="")
    @patch("src.cli.split_into_chunks", return_value=["x = 1\n"])
    @patch("src.cli.call_llm", return_value="ok")
    def test_single_chunk_no_diff(
        self, mock_llm, mock_chunks, mock_diff, mock_read, mock_val
    ) -> None:
        from src.cli import _analyze_file

        path, response, error, diff = _analyze_file("file.py", "rules")
        assert response == "ok"
