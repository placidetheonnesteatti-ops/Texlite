from __future__ import annotations

import html
import re
import unicodedata

SPECIALS = {
    "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
    "{": r"\{", "}": r"\}", "\\": r"\textbackslash{}",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}
UNICODE_MAP = {
    "–": "--", "—": "---", "…": r"\ldots{}", "“": "``", "”": "''", "„": "``", "’": "'", "‘": "'",
    " ": " ", " ": " ", "−": "-",
}
MATH_UNICODE_MAP = {
    "×": r"$\times$", "÷": r"$\div$", "≤": r"$\leq$", "≥": r"$\geq$", "≠": r"$\neq$",
}


def normalize_text(text: str, collapse_whitespace: bool = True) -> str:
    text = html.unescape(text or "")
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    for src, dst in UNICODE_MAP.items():
        text = text.replace(src, dst)
    if collapse_whitespace:
        text = re.sub(r"[ \t]+", " ", text)
    return text


def escape_latex(text: str, clean_text: bool = True) -> str:
    # Escaping remains mandatory even when the optional whitespace cleanup is disabled.
    text = normalize_text(text, collapse_whitespace=clean_text)
    escaped = "".join(SPECIALS.get(ch, ch) for ch in text)
    for src, dst in MATH_UNICODE_MAP.items():
        escaped = escaped.replace(src, dst)
    return escaped


def latex_comment(text: str) -> str:
    return "% " + text.replace("\n", " ")


def safe_filename(name: str, fallback: str = "document") -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip())
    name = name.strip("._")
    return name or fallback
