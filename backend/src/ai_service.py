"""LLM call service via kiro-cli subprocess.

Sends the assembled prompt to the LLM and returns the raw response.
Supports KIROSONAR_MOCK=1 for offline testing.
"""

import os
import re
import subprocess

# Regex que captura sequências de escape ANSI (cores, formatação, etc.)
_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")

# Mock responses específicos para cada tipo de arquivo de teste
_MOCK_RESPONSES: dict[str, str] = {
    "unused_vars": """\
## Bugs
- Nenhum bug encontrado.

## Vulnerabilidades
- Nenhuma vulnerabilidade encontrada.

## Code Smells
- Variável `unusedVar` declarada mas nunca utilizada (linha 3).

## Hotspots de Segurança
- Nenhum hotspot encontrado.

## Código Refatorado
[START]
function processData(input) {
    const result = input * 2;
    return result;
}
[END]
""",
    "unreachable_code": """\
## Bugs
- Código inalcançável após return (linha 4-5). Dead code detectado.

## Vulnerabilidades
- Nenhuma vulnerabilidade encontrada.

## Code Smells
- Nenhum code smell encontrado.

## Hotspots de Segurança
- Nenhum hotspot encontrado.

## Código Refatorado
[START]
function calculate(x) {
    return x * 2;
}
[END]
""",
    "duplicate_code": """\
## Bugs
- Nenhum bug encontrado.

## Vulnerabilidades
- Nenhuma vulnerabilidade encontrada.

## Code Smells
- Código duplicado detectado. Blocos repetidos nas funções.

## Hotspots de Segurança
- Nenhum hotspot encontrado.

## Código Refatorado
[START]
function processItem(item) {
    return item.value * 2;
}
[END]
""",
    "security_issues": """\
## Bugs
- Nenhum bug encontrado.

## Vulnerabilidades
- Uso de eval() detectado (linha 3). Vulnerabilidade de segurança crítica.

## Code Smells
- Nenhum code smell encontrado.

## Hotspots de Segurança
- eval() pode executar código arbitrário.

## Código Refatorado
[START]
function executeCode(code) {
    // Evite usar eval - use alternativas seguras
    return JSON.parse(code);
}
[END]
""",
    "code_smells": """\
## Bugs
- Nenhum bug encontrado.

## Vulnerabilidades
- Nenhuma vulnerabilidade encontrada.

## Code Smells
- Função muito longa com mais de 50 linhas. Considere refatorar.

## Hotspots de Segurança
- Nenhum hotspot encontrado.

## Código Refatorado
[START]
function processData(data) {
    return data.map(item => item * 2);
}
[END]
""",
    "comparisons": """\
## Bugs
- Uso de == ao invés de === (linhas 2, 5). Use igualdade estrita.

## Vulnerabilidades
- Nenhuma vulnerabilidade encontrada.

## Code Smells
- Comparação com == pode causar coerção de tipos inesperada.

## Hotspots de Segurança
- Nenhum hotspot encontrado.

## Código Refatorado
[START]
function checkValue(value) {
    if (value === null) {
        return false;
    }
    if (value === 0) {
        return false;
    }
    return true;
}
[END]
""",
    "console_logs": """\
## Bugs
- Nenhum bug encontrado.

## Vulnerabilidades
- Nenhuma vulnerabilidade encontrada.

## Code Smells
- console.log encontrado (linhas 2, 4). Remova logs de debug em produção.

## Hotspots de Segurança
- Nenhum hotspot encontrado.

## Código Refatorado
[START]
function processOrder(order) {
    const total = order.items.reduce((sum, item) => sum + item.price, 0);
    return total;
}
[END]
""",
    "global_vars": """\
## Bugs
- Variável global implícita detectada (linha 2). Use let, const ou var.

## Vulnerabilidades
- Nenhuma vulnerabilidade encontrada.

## Code Smells
- Falta declaração de variável com let/const/var.

## Hotspots de Segurança
- Nenhum hotspot encontrado.

## Código Refatorado
[START]
function setConfig() {
    const config = { debug: true };
    return config;
}
[END]
""",
    "callback_hell": """\
## Bugs
- Nenhum bug encontrado.

## Vulnerabilidades
- Nenhuma vulnerabilidade encontrada.

## Code Smells
- Callbacks aninhados em excesso (>3 níveis). Use async/await ou Promises.

## Hotspots de Segurança
- Nenhum hotspot encontrado.

## Código Refatorado
[START]
async function fetchData() {
    const data = await getData();
    const processed = await processData(data);
    const saved = await saveData(processed);
    return await notifyUser(saved);
}
[END]
""",
    "error_handling": """\
## Bugs
- try sem catch detectado (linha 2). Erro não tratado.

## Vulnerabilidades
- Nenhuma vulnerabilidade encontrada.

## Code Smells
- Falta tratamento de exceção adequado.

## Hotspots de Segurança
- Nenhum hotspot encontrado.

## Código Refatorado
[START]
function parseJSON(text) {
    try {
        return JSON.parse(text);
    } catch (error) {
        console.error('Parse error:', error);
        return null;
    }
}
[END]
""",
}

MOCK_RESPONSE_DEFAULT: str = """\
## Bugs
- Nenhum bug encontrado.

## Vulnerabilidades
- Nenhuma vulnerabilidade encontrada.

## Code Smells
- Variável com nome não descritivo (linha 10).

## Hotspots de Segurança
- Nenhum hotspot encontrado.

## Código Refatorado
[START]
def calcular_total(valor: float) -> float:
    return valor * 1.1
[END]
"""


def _get_mock_response(prompt: str) -> str:
    """Retorna resposta mock baseada no conteúdo do prompt.

    Args:
        prompt: Prompt enviado para análise.

    Returns:
        Resposta mock apropriada para o tipo de arquivo.
    """
    for file_key, response in _MOCK_RESPONSES.items():
        if file_key in prompt.lower():
            return response
    return MOCK_RESPONSE_DEFAULT


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from a string.

    Args:
        text: Raw string potentially containing terminal color codes.

    Returns:
        Clean string without ANSI sequences.
    """
    return _ANSI_ESCAPE_RE.sub("", text)


def call_llm(prompt: str) -> str:
    """Send a prompt to the LLM via kiro-cli and return the response.

    Uses stdin (pipe) to avoid OS argument-length limits on large prompts.
    Strips ANSI escape codes from the output so reports are clean Markdown.

    Args:
        prompt: Complete prompt string to be sent.

    Returns:
        LLM response (stdout) without ANSI codes.

    Raises:
        RuntimeError: If the subprocess fails.
    """
    if os.environ.get("KIROSONAR_MOCK") == "1":
        return _get_mock_response(prompt)

    # Envia o prompt via stdin para evitar limite de tamanho de argumento
    try:
        result = subprocess.run(
            ["kiro-cli", "chat", "--no-interactive", "--trust-tools="],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("Timeout: kiro-cli não respondeu em 120 segundos.")

    if result.returncode != 0:
        raise RuntimeError(f"Erro ao chamar kiro-cli: {result.stderr}")
    return _strip_ansi(result.stdout.strip())
