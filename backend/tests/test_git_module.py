"""Unit tests for src/git_module.py."""

import pytest
from unittest.mock import patch, mock_open, MagicMock

from src.git_module import get_changed_files, get_file_diff, read_file_content


class TestGetChangedFiles:
    """Tests for get_changed_files function."""

    @patch("src.git_module.subprocess.run")
    def test_returns_list_of_changed_files(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(
            returncode=0, stdout="src/foo.py\nsrc/bar.py\n", stderr=""
        )
        assert get_changed_files() == ["src/foo.py", "src/bar.py"]

    @patch("src.git_module.subprocess.run")
    def test_returns_empty_list_when_no_changes(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        assert get_changed_files() == []

    @patch("src.git_module.subprocess.run")
    def test_filters_empty_lines(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(
            returncode=0, stdout="src/foo.py\n\n\nsrc/bar.py\n", stderr=""
        )
        assert get_changed_files() == ["src/foo.py", "src/bar.py"]

    @patch("src.git_module.subprocess.run")
    def test_exits_when_not_a_git_repo(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(
            returncode=128, stdout="", stderr="fatal: not a git repository"
        )
        with pytest.raises(SystemExit) as exc_info:
            get_changed_files()
        assert exc_info.value.code == 1

    @patch("src.git_module.subprocess.run")
    def test_calls_correct_git_command(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        get_changed_files()
        mock_run.assert_called_once_with(
            ["git", "diff", "--name-only"], capture_output=True, text=True
        )


class TestGetFileDiff:
    """Tests for get_file_diff function."""

    @patch("src.git_module.subprocess.run")
    def test_returns_diff_output(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(
            returncode=0, stdout="@@ -1 +1 @@\n-old\n+new", stderr=""
        )
        assert get_file_diff("src/foo.py") == "@@ -1 +1 @@\n-old\n+new"

    @patch("src.git_module.subprocess.run")
    def test_returns_empty_when_no_diff(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        assert get_file_diff("src/foo.py") == ""

    @patch("src.git_module.subprocess.run")
    def test_returns_empty_on_error(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error")
        assert get_file_diff("src/foo.py") == ""

    @patch("src.git_module.subprocess.run")
    def test_calls_git_diff_with_file_path(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        get_file_diff("src/foo.py")
        mock_run.assert_called_once_with(
            ["git", "diff", "src/foo.py"], capture_output=True, text=True
        )


class TestReadFileContent:
    """Tests for read_file_content function."""

    def test_returns_file_content(self) -> None:
        fake_content = "print('hello world')\n"
        with patch("builtins.open", mock_open(read_data=fake_content)):
            assert read_file_content("src/foo.py") == fake_content

    def test_raises_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError):
            read_file_content("non_existent_file.py")
