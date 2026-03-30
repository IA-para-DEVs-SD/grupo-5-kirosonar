"""Unit tests for src.config module."""

import os
import tempfile

from src.config import DEFAULT_RULES, load_rules


class TestLoadRules:
    """Tests for the load_rules function."""

    def test_returns_default_rules_when_file_not_found(self) -> None:
        """Should return DEFAULT_RULES when the given path does not exist."""
        result = load_rules("nonexistent_file.md")
        assert result == DEFAULT_RULES

    def test_returns_default_rules_when_none_and_no_file_in_cwd(
        self, tmp_path, monkeypatch
    ) -> None:
        """Should return DEFAULT_RULES when path is None and regras_empresa.md is absent."""
        monkeypatch.chdir(tmp_path)
        result = load_rules(None)
        assert result == DEFAULT_RULES

    def test_returns_file_content_when_path_provided(self) -> None:
        """Should return the file content when a valid path is given."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Custom Rules")
            tmp = f.name
        try:
            result = load_rules(tmp)
            assert result == "# Custom Rules"
        finally:
            os.unlink(tmp)

    def test_returns_file_content_when_regras_exists_in_cwd(self, tmp_path, monkeypatch) -> None:
        """Should read regras_empresa.md from cwd when path is None."""
        rules_file = tmp_path / "regras_empresa.md"
        rules_file.write_text("# Regras do Time", encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        result = load_rules(None)
        assert result == "# Regras do Time"

    def test_default_rules_is_not_empty(self) -> None:
        """DEFAULT_RULES constant must not be empty."""
        assert len(DEFAULT_RULES.strip()) > 0
