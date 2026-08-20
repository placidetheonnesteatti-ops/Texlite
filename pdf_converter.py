from __future__ import annotations

from pathlib import Path

import fitz

from .latex_utils import escape_latex, safe_filename
from .models import ConversionOptions, ConversionResult
from .tex_writer import wrap_document


def _font_size_from_block(block) -> float:
    spans = []
    for line in block.get("lines", []):
        spans.extend(line.get("spans", []))
    if not spans:
        return 11.0
    return max(7.0, min(22.0, sum(float(s.get("size", 11.0)) for s in spans) / len(spans)))


def _block_text(block) -> str:
    lines = []
    for line in block.get("lines", []):
        txt = "".join(span.get("text", "") for span in line.get("spans", []))
        if txt.strip():
            lines.append(txt.rstrip())
    return "\n".join(lines).strip()


def _page_to_tex(page: fitz.Page, page_no: int, images_dir: Path, warnings: list[str], image_counter: list[int]) -> list[str]:
    width, height = page.rect.width, page.rect.height
    parts = [f"% --- Reconstructed PDF page {page_no} ({width:.1f}pt x {height:.1f}pt) ---"]
    blocks = page.get_text("dict").get("blocks", [])
    blocks = [b for b in blocks if b.get("type") == 0 and _block_text(b)]
    # A linear reconstruction is intentionally used for portability. We preserve block order,
    # estimated font size and explicit page boundaries while avoiding fragile absolute positioning.
    for block in blocks:
        text = _block_text(block)
        bbox = block.get("bbox", [0, 0, width, 12])
        size = _font_size_from_block(block)
        top = float(bbox[1])
        if top > 0:
            # A small vertical hint improves similarity without making the generated TeX brittle.
            parts.append(rf"\vspace*{{{min(1.5, top / 72 / 8):.2f}cm}}")
        safe = escape_latex(text).replace("\n", r"\\")
        parts.append(rf"{{\fontsize{{{size:.1f}pt}}{{{size * 1.2:.1f}pt}}\selectfont {safe}}}")
        parts.append(r"\par\vspace{0.15em}")

    for img in page.get_images(full=True):
        xref = img[0]
        try:
            data = page.parent.extract_image(xref)
        except Exception as exc:
            warnings.append(f"Image PDF page {page_no} non extraite : {exc}")
            continue
        image_counter[0] += 1
        fname = f"page_{page_no:03d}_image_{image_counter[0]:03d}.{data['ext']}"
        (images_dir / fname).write_bytes(data["image"])
        # Keep a readable size rather than stretching to the page edge.
        parts.append(rf"\begin{{figure}}[H]\centering\includegraphics[width=0.78\textwidth]{{images/{fname}}}\end{{figure}}")
    return parts


def convert_pdf(source: Path, options: ConversionOptions) -> ConversionResult:
    project = options.output_dir / f"{safe_filename(source.stem)}_latex"
    project.mkdir(parents=True, exist_ok=True)
    images_dir = project / "images"
    images_dir.mkdir(exist_ok=True)
    warnings = []
    try:
        pdf = fitz.open(source)
        parts: list[str] = []
        image_counter = [0]
        for page_no, page in enumerate(pdf, start=1):
            parts.extend(_page_to_tex(page, page_no, images_dir, warnings, image_counter))
            if page_no < len(pdf):
                parts.append(r"\newpage")
        tex_path = project / "main.tex"
        tex_path.write_text(wrap_document("\n\n".join(parts)), encoding="utf-8")
        warnings.append("PDF : reconstruction linéaire. Pour une copie visuelle quasi pixel-perfect, une retouche manuelle peut encore être nécessaire pour les mises en page complexes.")
        return ConversionResult(True, source, project, tex_path, None, len(pdf), None, image_counter[0], 0, warnings, [], "")
    except Exception as exc:
        return ConversionResult(False, source, project, None, None, None, None, 0, 0, warnings, [f"{type(exc).__name__}: {exc}"], "")
