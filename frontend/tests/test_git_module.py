"""Unit tests for src/git_module.py."""

import pytest
from unittest.mock import patch, mock_open, MagicMock

from src.git_module import get_changed_files, read_file_content


class TestGetChangedFiles:
    """Tests for get_changed_files function."""

    @patch("src.git_module.subprocess.run")
    def test_returns_list_of_changed_files(self, mock_run: MagicMock) -> None:
        """Should return a list of file paths when git diff has output."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="src/foo.py\nsrc/bar.py\n",
            stderr="",
        )

        result = get_changed_files()

        assert result == ["src/foo.py", "src/bar.py"]

    @patch("src.git_module.subprocess.run")
    def test_returns_empty_list_when_no_changes(self, mock_run: MagicMock) -> None:
        """Should return an empty list when there are no changed files."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr="",
        )

        result = get_changed_files()

        assert result == []

    @patch("src.git_module.subprocess.run")
    def test_filters_empty_lines(self, mock_run: MagicMock) -> None:
        """Should filter out blank lines from git diff output."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="src/foo.py\n\n\nsrc/bar.py\n",
            stderr="",
        )

        result = get_changed_files()

        assert result == ["src/foo.py", "src/bar.py"]

    @patch("src.git_module.subprocess.run")
    def test_exits_when_not_a_git_repo(self, mock_run: MagicMock) -> None:
        """Should call sys.exit(1) when not inside a Git repository."""
        mock_run.return_value = MagicMock(
            returncode=128,
            stdout="",
            stderr="fatal: not a git repository",
        )

        with pytest.raises(SystemExit) as exc_info:
            get_changed_files()

        assert exc_info.value.code == 1

    @patch("src.git_module.subprocess.run")
    def test_calls_correct_git_command(self, mock_run: MagicMock) -> None:
        """Should invoke subprocess with the correct git diff command."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        get_changed_files()

        mock_run.assert_called_once_with(
            ["git", "diff", "--name-only"],
            capture_output=True,
            text=True,
        )


class TestReadFileContent:
    """Tests for read_file_content function."""

    def test_returns_file_content(self) -> None:
        """Should return the full content of an existing file."""
        fake_content = "print('hello world')\n"

        with patch("builtins.open", mock_open(read_data=fake_content)):
            result = read_file_content("src/foo.py")

        assert result == fake_content

    def test_raises_file_not_found(self) -> None:
        """Should raise FileNotFoundError for a non-existent file."""
        with pytest.raises(FileNotFoundError):
            read_file_content("non_existent_file.py")
