"""Unit tests for src.cli module."""

import sys
from unittest.mock import patch, MagicMock

import pytest

from src.cli import _build_parser, _run_analyze, main


class TestBuildParser:
    """Tests for the _build_parser function."""

    def test_parser_has_analyze_subcommand(self) -> None:
        """Parser must recognize the 'analyze' subcommand."""
        parser = _build_parser()
        args = parser.parse_args(["analyze"])
        assert args.command == "analyze"

    def test_analyze_path_defaults_to_none(self) -> None:
        """--path should default to None when not provided."""
        parser = _build_parser()
        args = parser.parse_args(["analyze"])
        assert args.path is None

    def test_analyze_rules_defaults_to_none(self) -> None:
        """--rules should default to None when not provided."""
        parser = _build_parser()
        args = parser.parse_args(["analyze"])
        assert args.rules is None

    def test_analyze_accepts_path_flag(self) -> None:
        """--path should capture the provided value."""
        parser = _build_parser()
        args = parser.parse_args(["analyze", "--path", "src/app.py"])
        assert args.path == "src/app.py"

    def test_analyze_accepts_rules_flag(self) -> None:
        """--rules should capture the provided value."""
        parser = _build_parser()
        args = parser.parse_args(["analyze", "--rules", "rules.md"])
        assert args.rules == "rules.md"


class TestRunAnalyze:
    """Tests for the _run_analyze function."""

    def test_uses_path_when_provided(self, capsys) -> None:
        """When --path is given, should NOT call mock_get_changed_files."""
        parser = _build_parser()
        args = parser.parse_args(["analyze", "--path", "my_file.py"])
        _run_analyze(args)
        output = capsys.readouterr().out
        assert "my_file.py" in output
        assert "get_changed_files" not in output

    def test_uses_git_diff_when_no_path(self, capsys) -> None:
        """When --path is omitted, should call mock_get_changed_files."""
        parser = _build_parser()
        args = parser.parse_args(["analyze"])
        _run_analyze(args)
        output = capsys.readouterr().out
        assert "get_changed_files" in output


class TestMain:
    """Tests for the main entry point."""

    def test_no_command_prints_help(self, capsys) -> None:
        """Running without a subcommand should print help."""
        with patch("sys.argv", ["kirosonar"]):
            main()
        output = capsys.readouterr().out
        assert "usage:" in output.lower()

    def test_analyze_command_runs(self, capsys) -> None:
        """Running 'analyze' should execute the analysis flow."""
        with patch("sys.argv", ["kirosonar", "analyze"]):
            main()
        output = capsys.readouterr().out
        assert "Análise concluída" in output
