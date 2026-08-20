from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from .compiler import compile_tex, count_pdf_pages
from .docx_converter import convert_docx
from .models import ConversionOptions, ConversionResult
from .pdf_converter import convert_pdf


def _source_docx_pages(path: Path) -> int | None:
    soffice = shutil.which("libreoffice") or shutil.which("soffice")
    if not soffice:
        return None
    with tempfile.TemporaryDirectory(prefix="docu2tex_pages_") as td:
        out = Path(td)
        try:
            subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(out), str(path)], capture_output=True, text=True, timeout=120)
            pdf = out / f"{path.stem}.pdf"
            return count_pdf_pages(pdf) if pdf.exists() else None
        except Exception:
            return None


def _retune_pagination(tex_path: Path, target_pages: int | None, initial_pages: int | None, max_rounds: int = 2) -> tuple[int | None, list[str]]:
    if not target_pages or not initial_pages or target_pages == initial_pages:
        return initial_pages, []
    notices: list[str] = []
    text = tex_path.read_text(encoding="utf-8")
    candidates = [
        (r"\\setlength\{\\parskip\}\{[^}]+\}", r"\\setlength{\\parskip}{0.40em}"),
        (r"\\setlength\{\\parskip\}\{[^}]+\}", r"\\setlength{\\parskip}{0.30em}"),
    ] if initial_pages > target_pages else [
        (r"\\setlength\{\\parskip\}\{[^}]+\}", r"\\setlength{\\parskip}{0.70em}"),
        (r"\\setlength\{\\parskip\}\{[^}]+\}", r"\\setlength{\\parskip}{0.85em}"),
    ]
    current = initial_pages
    for idx, (pattern, replacement) in enumerate(candidates[:max_rounds], start=1):
        new = re.sub(pattern, replacement, tex_path.read_text(encoding="utf-8"), count=1)
        if new == tex_path.read_text(encoding="utf-8"):
            break
        tex_path.write_text(new, encoding="utf-8")
        ok, pdf, _ = compile_tex(tex_path, passes=2)
        if not ok or not pdf:
            break
        current = count_pdf_pages(pdf)
        notices.append(f"Ajustement pagination {idx}: {current} page(s).")
        if current == target_pages:
            break
    return current, notices


def convert_file(source: Path, options: ConversionOptions, progress=None) -> ConversionResult:
    if progress:
        progress("Analyse du document", 10)
    ext = source.suffix.lower()
    if ext == ".docx":
        result = convert_docx(source, options)
        result.source_pages = _source_docx_pages(source)
    elif ext == ".pdf":
        result = convert_pdf(source, options)
    else:
        return ConversionResult(False, source, errors=["Format non pris en charge. Utilisez DOCX ou PDF."])
    if not result.success:
        return result
    if progress:
        progress("LaTeX généré", 55)
    if options.compile_pdf and result.tex_path:
        if progress:
            progress("Compilation LaTeX", 70)
        ok, pdf, log = compile_tex(result.tex_path)
        result.log = log
        if ok and pdf:
            result.pdf_path = pdf
            result.output_pages = count_pdf_pages(pdf)
            if result.source_pages and result.output_pages and result.source_pages != result.output_pages and options.optimize_pagination:
                tuned_pages, notices = _retune_pagination(result.tex_path, result.source_pages, result.output_pages)
                result.output_pages = tuned_pages
                result.log += "\n" + "\n".join(notices)
                result.warnings.extend(notices)
            if result.source_pages and result.output_pages:
                delta = result.output_pages - result.source_pages
                if delta:
                    result.warnings.append(f"Pagination : source {result.source_pages} page(s), résultat {result.output_pages} page(s). Écart de {delta:+d}.")
        else:
            result.warnings.append("Le projet LaTeX a été généré, mais le PDF n'a pas pu être compilé sur cette machine.")
    if progress:
        progress("Contrôle terminé", 100)
    return result
