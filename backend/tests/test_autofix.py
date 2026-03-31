"""Unit tests for src.autofix module."""

import os
from unittest.mock import mock_open, patch

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from src.autofix import apply_fix, extract_refactored_code


class TestExtractRefactoredCode:
    """Tests for extract_refactored_code."""

    def test_extracts_code_between_tags(self) -> None:
        response = "## Bugs\n- None\n\n## Código Refatorado\n[START]\ndef foo():\n    pass\n[END]"
        assert extract_refactored_code(response) == "def foo():\n    pass"

    def test_returns_none_when_no_tags(self) -> None:
        assert extract_refactored_code("## Bugs\n- None") is None

    def test_returns_none_when_only_start_tag(self) -> None:
        assert extract_refactored_code("[START]\ndef foo(): pass") is None

    def test_returns_none_when_only_end_tag(self) -> None:
        assert extract_refactored_code("def foo(): pass\n[END]") is None

    def test_extracts_multiline_code(self) -> None:
        code = "def foo():\n    x = 1\n    return x"
        response = f"[START]\n{code}\n[END]"
        assert extract_refactored_code(response) == code

    def test_returns_none_on_empty_string(self) -> None:
        assert extract_refactored_code("") is None

    def test_handles_whitespace_around_tags(self) -> None:
        response = "[START]   \ndef bar(): pass\n   [END]"
        result = extract_refactored_code(response)
        assert result is not None
        assert "def bar(): pass" in result

    @given(st.text(min_size=1))
    @settings(max_examples=100)
    def test_never_raises_on_arbitrary_input(self, text: str) -> None:
        """extract_refactored_code must never raise for any string input."""
        result = extract_refactored_code(text)
        assert result is None or isinstance(result, str)


class TestApplyFix:
    """Tests for apply_fix."""

    def test_returns_false_when_no_code_in_response(self, capsys) -> None:
        result = apply_fix("## Bugs\n- None", "file.py")
        assert result is False
        assert "Nenhum código refatorado" in capsys.readouterr().out

    def test_returns_false_when_user_declines(self, tmp_path) -> None:
        file = tmp_path / "app.py"
        file.write_text("old code")
        response = "[START]\nnew code\n[END]"
        with patch("builtins.input", return_value="n"):
            result = apply_fix(response, str(file))
        assert result is False
        assert file.read_text() == "old code"

    def test_applies_fix_and_creates_backup_when_user_confirms(self, tmp_path) -> None:
        file = tmp_path / "app.py"
        file.write_text("old code")
        response = "[START]\nnew code\n[END]"
        with patch("builtins.input", return_value="s"):
            result = apply_fix(response, str(file))
        assert result is True
        assert file.read_text() == "new code"
        assert (tmp_path / "app.py.bak").read_text() == "old code"

    def test_backup_file_created_before_overwrite(self, tmp_path) -> None:
        file = tmp_path / "script.py"
        original = "original content"
        file.write_text(original)
        response = "[START]\nrefactored\n[END]"
        with patch("builtins.input", return_value="s"):
            apply_fix(response, str(file))
        backup = tmp_path / "script.py.bak"
        assert backup.exists()
        assert backup.read_text() == original

    def test_prints_preview_before_asking(self, tmp_path, capsys) -> None:
        file = tmp_path / "app.py"
        file.write_text("x = 1")
        response = "[START]\ny = 2\n[END]"
        with patch("builtins.input", return_value="n"):
            apply_fix(response, str(file))
        output = capsys.readouterr().out
        assert "y = 2" in output
