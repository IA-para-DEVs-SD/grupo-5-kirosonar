"""Unit tests for src.chunker module."""

from src.chunker import (
    MIN_LINES_FOR_CHUNKING,
    _apply_overlap,
    _chunk_by_size,
    split_into_chunks,
)


class TestSplitIntoChunks:
    """Tests for split_into_chunks."""

    def test_small_file_returns_single_chunk(self) -> None:
        code = "line\n" * 10
        result = split_into_chunks(code)
        assert result == [code]

    def test_file_at_threshold_returns_single_chunk(self) -> None:
        code = "x = 1\n" * MIN_LINES_FOR_CHUNKING
        result = split_into_chunks(code)
        assert result == [code]

    def test_large_file_with_boundaries_returns_multiple_chunks(self) -> None:
        # Build a file with 400+ lines and function boundaries
        lines = []
        for i in range(5):
            lines.append(f"def func_{i}():\n")
            lines.extend([f"    x = {j}\n" for j in range(80)])
        code = "".join(lines)
        result = split_into_chunks(code, "test.py")
        assert len(result) >= 1

    def test_large_file_no_boundaries_falls_back_to_size(self) -> None:
        # 400 lines with no function/class boundaries
        code = "x = 1\n" * 400
        result = split_into_chunks(code)
        assert len(result) >= 2

    def test_returns_list_of_strings(self) -> None:
        code = "def foo():\n    pass\n" * 200
        result = split_into_chunks(code)
        assert all(isinstance(c, str) for c in result)

    def test_single_boundary_falls_back_to_size(self) -> None:
        lines = ["def only_one():\n"] + ["    x = 1\n"] * 400
        code = "".join(lines)
        result = split_into_chunks(code)
        assert len(result) >= 2


class TestChunkBySize:
    """Tests for _chunk_by_size."""

    def test_small_input_returns_single_chunk(self) -> None:
        lines = ["line\n"] * 50
        result = _chunk_by_size(lines)
        assert len(result) == 1

    def test_large_input_returns_multiple_chunks(self) -> None:
        lines = ["x = 1\n"] * 400
        result = _chunk_by_size(lines)
        assert len(result) >= 2

    def test_cuts_at_empty_lines_when_possible(self) -> None:
        lines = ["x = 1\n"] * 95 + ["\n"] + ["y = 2\n"] * 200
        result = _chunk_by_size(lines)
        assert len(result) >= 2

    def test_cuts_at_closing_brace(self) -> None:
        lines = ["x = 1\n"] * 95 + ["}\n"] + ["y = 2\n"] * 200
        result = _chunk_by_size(lines)
        assert len(result) >= 2


class TestApplyOverlap:
    """Tests for _apply_overlap."""

    def test_first_chunk_unchanged(self) -> None:
        lines = [f"line {i}\n" for i in range(200)]
        chunks = ["".join(lines[:100]), "".join(lines[100:])]
        boundaries = [0, 100]
        result = _apply_overlap(lines, boundaries, chunks)
        assert result[0] == chunks[0]

    def test_subsequent_chunks_have_overlap_context(self) -> None:
        lines = [f"line {i}\n" for i in range(200)]
        chunks = ["".join(lines[:100]), "".join(lines[100:])]
        boundaries = [0, 100]
        result = _apply_overlap(lines, boundaries, chunks)
        assert "contexto do trecho anterior" in result[1]
