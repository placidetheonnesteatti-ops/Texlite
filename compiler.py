from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def find_latex_engine() -> str | None:
    # The generated preamble uses fontspec and polyglossia, which require XeLaTeX or LuaLaTeX.
    for candidate in ("xelatex", "lualatex"):
        path = shutil.which(candidate)
        if path:
            return path
    return None


def compile_tex(tex_path: Path, passes: int = 2) -> tuple[bool, Path | None, str]:
    engine = find_latex_engine()
    if not engine:
        return False, None, "Aucun moteur LaTeX compatible (XeLaTeX ou LuaLaTeX) n'a été trouvé. Installez MiKTeX ou TeX Live."
    logs: list[str] = []
    cwd = tex_path.parent
    for i in range(max(1, passes)):
        proc = subprocess.run(
            [engine, "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
        )
        logs.append(f"Pass {i+1}: returncode={proc.returncode}\n{proc.stdout[-5000:]}\n{proc.stderr[-2000:]}")
        if proc.returncode != 0:
            return False, None, "\n".join(logs)
    pdf = tex_path.with_suffix(".pdf")
    return pdf.exists(), pdf if pdf.exists() else None, "\n".join(logs)


def count_pdf_pages(pdf: Path) -> int | None:
    try:
        import fitz
        return len(fitz.open(pdf))
    except Exception:
        return None
