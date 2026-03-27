"""Configuration module for loading analysis rules.

Reads the company rules file (.md) and provides a generic
best-practices fallback when the file does not exist.
"""

import os

DEFAULT_RULES: str = """\
# Regras Gerais de Código Limpo
1. Funções devem ter responsabilidade única (SRP).
2. Nomes de variáveis e funções devem ser descritivos.
3. Evite código duplicado — extraia funções reutilizáveis.
4. Trate exceções de forma explícita; nunca use except genérico.
5. Mantenha funções curtas (máx. ~20 linhas).
6. Use type hints em todas as assinaturas.
7. Remova imports não utilizados e código morto.
8. Prefira constantes nomeadas a valores mágicos.
9. Escreva docstrings para módulos e funções públicas.
10. Siga a PEP 8 para formatação e estilo.
"""


def load_rules(rules_path: str | None = None) -> str:
    """Load analysis rules from a .md file.

    Args:
        rules_path: Path to the rules file.
                    If None, looks for 'regras_empresa.md' in the current directory.

    Returns:
        String with the rules content. If the file does not exist,
        returns the DEFAULT_RULES constant defined in this module.
    """
    path = rules_path or os.path.join(os.getcwd(), "regras_empresa.md")

    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    return DEFAULT_RULES
