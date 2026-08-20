from pathlib import Path

from docx import Document
from docx.shared import Cm
from PIL import Image

from core.docx_converter import convert_docx
from core.models import ConversionOptions


def test_docx_image_dimension_is_preserved(tmp_path: Path):
    image = tmp_path / "img.png"
    Image.new("RGB", (300, 150), "white").save(image)
    source = tmp_path / "image.docx"
    doc = Document()
    doc.add_picture(str(image), width=Cm(5.0))
    doc.save(source)
    result = convert_docx(source, ConversionOptions(output_dir=tmp_path))
    assert result.success
    text = result.tex_path.read_text(encoding="utf-8")
    assert "width=5.00cm" in text
    assert (result.project_dir / "images" / "image_001.png").exists()
