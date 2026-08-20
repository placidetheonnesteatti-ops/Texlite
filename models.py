from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ConversionOptions:
    output_dir: Path
    compile_pdf: bool = True
    open_output: bool = False
    fidelity: str = "balanced"
    preserve_page_breaks: bool = True
    preserve_images: bool = True
    optimize_tables: bool = True
    clean_text: bool = True
    optimize_pagination: bool = True


@dataclass
class ConversionResult:
    success: bool
    source: Path
    project_dir: Path | None = None
    tex_path: Path | None = None
    pdf_path: Path | None = None
    source_pages: int | None = None
    output_pages: int | None = None
    images: int = 0
    tables: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    log: str = ""

    @property
    def status_text(self) -> str:
        return "Conversion terminée" if self.success else "Conversion échouée"
