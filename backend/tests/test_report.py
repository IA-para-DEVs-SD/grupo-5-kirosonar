"""Unit tests for src.report module."""

import os
from datetime import datetime

from src.report import generate_report_name, list_reports, save_report


class TestListReports:
    """Tests for the list_reports function."""

    def test_returns_empty_when_dir_does_not_exist(self) -> None:
        result = list_reports("/nonexistent/path")
        assert result == []

    def test_returns_empty_when_dir_is_empty(self, tmp_path) -> None:
        result = list_reports(str(tmp_path))
        assert result == []

    def test_returns_entry_for_each_report_file(self, tmp_path) -> None:
        (tmp_path / "report_a.md").write_text("# A")
        (tmp_path / "report_b.md").write_text("# B")
        result = list_reports(str(tmp_path))
        assert len(result) == 2

    def test_entry_has_correct_name(self, tmp_path) -> None:
        (tmp_path / "my_report.md").write_text("content")
        result = list_reports(str(tmp_path))
        assert result[0].name == "my_report.md"

    def test_entry_has_correct_size(self, tmp_path) -> None:
        content = "hello"
        (tmp_path / "report.md").write_text(content, encoding="utf-8")
        result = list_reports(str(tmp_path))
        assert result[0].size_bytes == len(content.encode("utf-8"))

    def test_entry_generated_at_is_datetime(self, tmp_path) -> None:
        (tmp_path / "report.md").write_text("x")
        result = list_reports(str(tmp_path))
        assert isinstance(result[0].generated_at, datetime)

    def test_sorted_most_recent_first(self, tmp_path) -> None:
        old = tmp_path / "old_report.md"
        new = tmp_path / "new_report.md"
        old.write_text("old")
        new.write_text("new")

        # Force different mtimes
        os.utime(old, (1_000_000, 1_000_000))
        os.utime(new, (2_000_000, 2_000_000))

        result = list_reports(str(tmp_path))
        assert result[0].name == "new_report.md"
        assert result[1].name == "old_report.md"

    def test_ignores_subdirectories(self, tmp_path) -> None:
        (tmp_path / "subdir").mkdir()
        (tmp_path / "report.md").write_text("content")
        result = list_reports(str(tmp_path))
        assert len(result) == 1
        assert result[0].name == "report.md"


class TestSaveReport:
    """Tests for save_report."""

    def test_creates_file_with_correct_content(self, tmp_path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        path = save_report("# Report", "src/app.py")
        assert os.path.isfile(path)
        with open(path, encoding="utf-8") as f:
            assert f.read() == "# Report"

    def test_creates_relatorios_dir_if_missing(self, tmp_path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        save_report("content", "file.py")
        assert (tmp_path / "relatorios").is_dir()


class TestGenerateReportName:
    """Tests for generate_report_name."""

    def test_contains_sanitized_path_and_timestamp(self) -> None:
        name = generate_report_name("src/app.py")
        assert "src_app_py" in name
        assert name.startswith("relatorios/")
        assert name.endswith(".md")
