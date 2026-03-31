"""Geração e salvamento de relatórios em Markdown."""

import os
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ReportEntry:
    """Representa um relatório encontrado na pasta relatorios/."""

    name: str
    generated_at: datetime
    size_bytes: int


def generate_report_name(file_path: str) -> str:
    """Gera o nome do arquivo de relatório baseado no arquivo analisado.

    Args:
        file_path: Caminho do arquivo original (ex: 'src/app.py').

    Returns:
        Nome do relatório com timestamp (ex: 'relatorios/src_app_py_20260318_173000.md').
    """
    safe_name = file_path.replace(os.sep, "_").replace("/", "_").replace(".", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join("relatorios", f"{safe_name}_{timestamp}.md")


def list_reports(reports_dir: str = "relatorios") -> list[ReportEntry]:
    """Lista os relatórios existentes na pasta relatorios/, ordenados por data (mais recente primeiro).

    Args:
        reports_dir: Caminho da pasta de relatórios.

    Returns:
        Lista de ReportEntry ordenada por data decrescente.
    """
    if not os.path.isdir(reports_dir):
        return []

    entries = []
    for name in os.listdir(reports_dir):
        full_path = os.path.join(reports_dir, name)
        if not os.path.isfile(full_path):
            continue
        stat = os.stat(full_path)
        entries.append(
            ReportEntry(
                name=name,
                generated_at=datetime.fromtimestamp(stat.st_mtime),
                size_bytes=stat.st_size,
            )
        )

    entries.sort(key=lambda e: e.generated_at, reverse=True)
    return entries


def save_report(content: str, file_path: str) -> str:
    """Salva o relatório da análise em um arquivo Markdown.

    Args:
        content: String Markdown retornada pela LLM.
        file_path: Caminho do arquivo original analisado.

    Returns:
        Caminho absoluto do arquivo de relatório salvo.
    """
    report_name = generate_report_name(file_path)
    os.makedirs(os.path.dirname(report_name), exist_ok=True)
    with open(report_name, "w", encoding="utf-8") as f:
        f.write(content)
    return os.path.abspath(report_name)
