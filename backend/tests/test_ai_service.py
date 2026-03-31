"""Unit tests for src.ai_service module."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from src.ai_service import _strip_ansi, call_llm


class TestStripAnsi:
    """Tests for _strip_ansi."""

    def test_removes_ansi_codes(self) -> None:
        assert _strip_ansi("\x1b[31mhello\x1b[0m") == "hello"

    def test_returns_clean_string_unchanged(self) -> None:
        assert _strip_ansi("hello world") == "hello world"


class TestCallLlm:
    """Tests for call_llm."""

    @patch.dict("os.environ", {"KIROSONAR_MOCK": "1"})
    def test_mock_returns_response_for_known_file(self) -> None:
        result = call_llm("analyze unused_vars.js")
        assert "unusedVar" in result

    @patch.dict("os.environ", {"KIROSONAR_MOCK": "1"})
    def test_mock_returns_default_for_unknown_file(self) -> None:
        result = call_llm("analyze something_random")
        assert "[START]" in result

    @patch.dict("os.environ", {"KIROSONAR_MOCK": "0"})
    @patch("src.ai_service.subprocess.run")
    def test_success_returns_stdout(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="## Bugs\n- None", stderr="")
        result = call_llm("prompt")
        assert result == "## Bugs\n- None"

    @patch.dict("os.environ", {"KIROSONAR_MOCK": "0"})
    @patch("src.ai_service.subprocess.run")
    def test_error_raises_runtime_error(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="fail")
        with pytest.raises(RuntimeError, match="Erro ao chamar kiro-cli"):
            call_llm("prompt")

    @patch.dict("os.environ", {"KIROSONAR_MOCK": "0"})
    @patch(
        "src.ai_service.subprocess.run",
        side_effect=subprocess.TimeoutExpired(cmd="k", timeout=120),
    )
    def test_timeout_raises_runtime_error(self, mock_run: MagicMock) -> None:
        with pytest.raises(RuntimeError, match="Timeout"):
            call_llm("prompt")
