"""Chunking de código por fronteiras de função/classe.

Divide arquivos grandes em pedaços lógicos para análise individual,
respeitando limites de função, método e classe.
"""

import re

# Padrões que indicam início de bloco em diversas linguagens
_BOUNDARY_RE = re.compile(
    r"^\s*(?:"
    r"(?:public|private|protected|static|async|export|abstract|final)\s+)*"
    r"(?:def |function\s|class\s|interface\s|trait\s|enum\s)",
    re.MULTILINE,
)

# Tamanho alvo de cada chunk em linhas
_TARGET_CHUNK_LINES: int = 100

# Linhas de overlap entre chunks consecutivos
_OVERLAP_LINES: int = 20

# Arquivos abaixo deste limite não precisam de chunking
MIN_LINES_FOR_CHUNKING: int = 300


def split_into_chunks(code: str, file_path: str = "") -> list[str]:
    """Divide código em chunks por fronteiras de função/classe.

    Args:
        code: Código fonte completo.
        file_path: Caminho do arquivo (para contexto).

    Returns:
        Lista de chunks. Se o arquivo for pequeno, retorna [code].
    """
    lines = code.splitlines(keepends=True)

    if len(lines) <= MIN_LINES_FOR_CHUNKING:
        return [code]

    # Encontra linhas que são fronteiras de bloco
    boundaries: list[int] = []
    for i, line in enumerate(lines):
        if _BOUNDARY_RE.match(line):
            boundaries.append(i)

    # Se não encontrou fronteiras suficientes, faz chunking por tamanho
    if len(boundaries) < 2:
        return _chunk_by_size(lines)

    # Agrupa fronteiras em chunks de ~_TARGET_CHUNK_LINES com overlap
    chunks: list[str] = []
    chunk_start = 0

    for boundary in boundaries:
        if boundary == chunk_start:
            continue
        if boundary - chunk_start >= _TARGET_CHUNK_LINES:
            chunks.append("".join(lines[chunk_start:boundary]))
            # Próximo chunk começa _OVERLAP_LINES antes da fronteira
            chunk_start = max(boundary - _OVERLAP_LINES, chunk_start)
            chunk_start = boundary  # fronteira real, overlap vem do anterior

    # Último chunk
    if chunk_start < len(lines):
        chunks.append("".join(lines[chunk_start:]))

    # Aplica overlap: cada chunk (exceto o primeiro) inclui linhas do anterior
    if len(chunks) > 1:
        chunks = _apply_overlap(lines, boundaries, chunks)

    return chunks if len(chunks) > 1 else [code]


def _apply_overlap(lines: list[str], boundaries: list[int], chunks: list[str]) -> list[str]:
    """Adiciona overlap entre chunks consecutivos.

    Cada chunk (exceto o primeiro) recebe as últimas _OVERLAP_LINES
    do chunk anterior como contexto.

    Args:
        lines: Todas as linhas do arquivo original.
        boundaries: Índices das fronteiras de função/classe.
        chunks: Chunks já divididos sem overlap.

    Returns:
        Chunks com overlap aplicado.
    """
    result = [chunks[0]]
    # Descobre onde cada chunk original começa
    pos = 0
    starts = [0]
    for chunk in chunks[:-1]:
        pos += len(chunk.splitlines(keepends=True))
        starts.append(pos)

    for i in range(1, len(chunks)):
        overlap_start = max(starts[i] - _OVERLAP_LINES, 0)
        overlap = "".join(lines[overlap_start : starts[i]])
        result.append(
            f"# ... contexto do trecho anterior ...\n{overlap}"
            f"# ... início deste trecho ...\n{chunks[i]}"
        )
    return result


def _chunk_by_size(lines: list[str]) -> list[str]:
    """Fallback: divide por tamanho, cortando em linhas seguras.

    Procura linhas em branco, fechamento de bloco ou indentação zero
    próximas ao target pra não cortar no meio de um bloco.

    Args:
        lines: Lista de linhas do arquivo.

    Returns:
        Lista de chunks respeitando pausas naturais do código.
    """
    chunks: list[str] = []
    chunk_start = 0
    total = len(lines)

    while chunk_start < total:
        # Se o que sobrou cabe num chunk, pega tudo
        if total - chunk_start <= _TARGET_CHUNK_LINES + 30:
            chunks.append("".join(lines[chunk_start:]))
            break

        # Procura linha segura pra cortar entre target e target+50
        best_cut = chunk_start + _TARGET_CHUNK_LINES
        for i in range(
            min(best_cut + 50, total) - 1,
            max(best_cut - 30, chunk_start),
            -1,
        ):
            stripped = lines[i].strip()
            if stripped == "" or stripped in ("}", "};", "end", "?>"):
                best_cut = i + 1
                break

        best_cut = min(best_cut, total)
        chunks.append("".join(lines[chunk_start:best_cut]))
        # Próximo chunk começa com overlap
        chunk_start = max(best_cut - _OVERLAP_LINES, chunk_start + 1)

    return chunks
