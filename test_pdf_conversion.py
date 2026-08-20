from pathlib import Path

import fitz
import pytest

from core.pdf_converter import convert_pdf
from core.models import ConversionOptions
from core.compiler import compile_tex


@pytest.mark.integration
def test_pdf_to_tex_and_compile(tmp_path: Path):
    src = tmp_path / "source.pdf"
    pdf = fitz.open()
    page = pdf.new_page()
    page.insert_text((72, 72), "Document PDF 50% & test")
    pdf.save(src)
    pdf.close()

    result = convert_pdf(src, ConversionOptions(output_dir=tmp_path))
    assert result.success
    assert result.source_pages == 1
    text = result.tex_path.read_text(encoding="utf-8")
    assert "Document PDF 50\\% \\& test" in text
    ok, out_pdf, _ = compile_tex(result.tex_path, passes=2)
    assert ok
    assert out_pdf and out_pdf.exists()
