"""Unit tests for src.prompt_builder module."""

from src.prompt_builder import _sanitize_user_content, build_prompt


class TestSanitizeUserContent:
    """Tests for _sanitize_user_content."""

    def test_removes_markers_case_insensitive(self) -> None:
        text = "hello [System] world [INST] end"
        result = _sanitize_user_content(text)
        assert "[System]" not in result
        assert "[INST]" not in result
        assert "hello" in result

    def test_removes_backticks(self) -> None:
        assert "```" not in _sanitize_user_content("code ```here```")

    def test_clean_text_unchanged(self) -> None:
        assert _sanitize_user_content("normal code") == "normal code"


class TestBuildPrompt:
    """Tests for build_prompt."""

    def test_includes_diff_section_when_diff_provided(self) -> None:
        result = build_prompt("@@ -1 +1 @@", "code", "rules", "f.py")
        assert "PESO MÁXIMO" in result

    def test_excludes_diff_section_when_empty(self) -> None:
        result = build_prompt("", "code", "rules", "f.py")
        assert "PESO MÁXIMO" not in result
from hypothesis import given, settings
from hypothesis import strategies as st

from src.prompt_builder import build_prompt


class TestBuildPrompt:
    """Tests for build_prompt."""

    def test_contains_file_path(self) -> None:
        result = build_prompt("", "code", "rules", "src/app.py")
        assert "src/app.py" in result

    def test_contains_rules(self) -> None:
        result = build_prompt("", "code", "# Use SOLID", "app.py")
        assert "# Use SOLID" in result

    def test_contains_full_code(self) -> None:
        result = build_prompt("", "def foo(): pass", "rules", "app.py")
        assert "def foo(): pass" in result

    def test_diff_section_included_when_diff_provided(self) -> None:
        result = build_prompt("@@ -1 +1 @@\n-old\n+new", "code", "rules", "app.py")
        assert "Diff das Alterações" in result
        assert "@@ -1 +1 @@" in result

    def test_diff_section_excluded_when_diff_empty(self) -> None:
        result = build_prompt("", "code", "rules", "app.py")
        assert "Diff das Alterações" not in result

    def test_contains_response_template_sections(self) -> None:
        result = build_prompt("", "code", "rules", "app.py")
        for section in ["## Bugs", "## Vulnerabilidades", "## Code Smells", "## Hotspots de Segurança", "## Código Refatorado"]:
            assert section in result

    def test_contains_start_end_tags_in_template(self) -> None:
        result = build_prompt("", "code", "rules", "app.py")
        assert "[START]" in result
        assert "[END]" in result

    def test_returns_string(self) -> None:
        assert isinstance(build_prompt("diff", "code", "rules", "file.py"), str)

    def test_empty_diff_does_not_produce_empty_prompt(self) -> None:
        result = build_prompt("", "", "", "")
        assert len(result) > 0

    @given(
        diff=st.text(),
        code=st.text(),
        rules=st.text(),
        file_path=st.text(min_size=1),
    )
    @settings(max_examples=100)
    def test_always_returns_non_empty_string(
        self, diff: str, code: str, rules: str, file_path: str
    ) -> None:
        """build_prompt must always return a non-empty string for any input."""
        result = build_prompt(diff, code, rules, file_path)
        assert isinstance(result, str)
        assert len(result) > 0

    @given(file_path=st.text(min_size=1, max_size=200))
    @settings(max_examples=50)
    def test_file_path_always_present_in_output(self, file_path: str) -> None:
        """The file_path must always appear in the generated prompt."""
        result = build_prompt("", "code", "rules", file_path)
        assert file_path in result
