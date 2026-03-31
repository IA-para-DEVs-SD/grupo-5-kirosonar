"""Unit tests for src.cli module."""

from unittest.mock import patch

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

    def test_no_command_prints_help(self, capsys) -> None:
        with patch("sys.argv", ["kirosonar"]):
            main()
        output = capsys.readouterr().out
        assert "usage:" in output.lower()

    @patch("src.cli.apply_fix")
    @patch("src.cli.save_report", return_value="/tmp/report.md")
    @patch("src.cli.call_llm", return_value="## Bugs\n- Nenhum")
    @patch("src.cli.read_file_content", return_value="print('hello')")
    def test_analyze_with_path_runs_full_flow(
        self, mock_read, mock_llm, mock_report, mock_fix, capsys
    ) -> None:
        """--path should skip git diff and run the full pipeline."""
        with patch("sys.argv", ["kirosonar", "analyze", "--path", "file.py"]):
            main()
        output = capsys.readouterr().out
        assert "Analisando: file.py" in output
        mock_read.assert_called_once_with("file.py")
        mock_llm.assert_called_once()
        mock_report.assert_called_once()
        mock_fix.assert_called_once()

    @patch("src.cli.apply_fix")
    @patch("src.cli.save_report", return_value="/tmp/report.md")
    @patch("src.cli.call_llm", return_value="## Bugs\n- Nenhum")
    @patch("src.cli.read_file_content", return_value="print('hello')")
    @patch("src.cli.get_file_diff", return_value="@@ -1 +1 @@\n-old\n+new")
    @patch("src.cli.get_changed_files", return_value=["src/app.py"])
    def test_analyze_git_flow_includes_diff(
        self, mock_files, mock_diff, mock_read, mock_llm, mock_report, mock_fix, capsys
    ) -> None:
        """Without --path, should call get_file_diff for each changed file."""
        with patch("sys.argv", ["kirosonar", "analyze"]):
            main()
        mock_diff.assert_called_once_with("src/app.py")
        mock_llm.assert_called_once()

    @patch("src.cli.get_changed_files", return_value=[])
    def test_analyze_no_files_prints_message(self, mock_git, capsys) -> None:
        with patch("sys.argv", ["kirosonar", "analyze"]):
            main()
        output = capsys.readouterr().out
        assert "Nenhum arquivo alterado encontrado" in output

    @patch("src.cli.read_file_content", side_effect=FileNotFoundError)
    def test_analyze_missing_file_skips_gracefully(self, mock_read, capsys) -> None:
        """--path with non-existent file should print warning and continue."""
        with patch("sys.argv", ["kirosonar", "analyze", "--path", "ghost.py"]):
            main()
        output = capsys.readouterr().out
        assert "Arquivo não encontrado" in output


class TestReportCommand:
    """Tests for the 'report' subcommand."""

    @patch("src.cli.list_reports", return_value=[])
    def test_report_empty_prints_no_reports(self, mock_list, capsys) -> None:
        with patch("sys.argv", ["kirosonar", "report"]):
            main()
        output = capsys.readouterr().out
        assert "Nenhum relatório encontrado." in output

    @patch("src.cli.list_reports")
    def test_report_lists_entries(self, mock_list, capsys) -> None:
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
