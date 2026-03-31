"""Unit tests for src.__main__ module."""

import runpy
from unittest.mock import patch


def test_main_module_calls_main() -> None:
    with patch("src.cli.main") as mock_main:
        runpy.run_module("src", run_name="__main__")
        mock_main.assert_called_once()
