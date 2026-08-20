from core.latex_utils import escape_latex


def test_escape_special_chars():
    assert escape_latex("50% & A_B #1") == r"50\% \& A\_B \#1"


def test_unicode_cleanup():
    assert "--" in escape_latex("A–B")


def test_escape_backslash_ascii_and_math_symbols():
    text = escape_latex(r"A\B ~ ^ × ÷ ≤ ≥ ≠")
    assert r"\textbackslash{}" in text
    assert r"\textasciitilde{}" in text
    assert r"\textasciicircum{}" in text
    assert r"$\times$" in text
    assert r"$\div$" in text
    assert r"$\leq$" in text
    assert r"$\geq$" in text
    assert r"$\neq$" in text
