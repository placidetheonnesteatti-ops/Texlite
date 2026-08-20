from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TexDocument:
    body: str
    image_count: int = 0
    table_count: int = 0
    warnings: list[str] | None = None


def preamble(font_size: str = "12pt", geometry: str = "top=2.5cm,bottom=2.5cm,left=2.5cm,right=2.5cm") -> str:
    return rf"""\documentclass[{font_size},a4paper]{{article}}
\usepackage{{fontspec}}
\usepackage{{polyglossia}}
\setmainlanguage{{french}}
\usepackage{{geometry}}
\geometry{{{geometry}}}
\usepackage{{graphicx}}
\usepackage{{array}}
\usepackage{{tabularx}}
\usepackage{{longtable}}
\usepackage{{booktabs}}
\usepackage{{float}}
\usepackage{{caption}}
\captionsetup{{font=small}}
\usepackage{{enumitem}}
\usepackage{{xcolor}}
\usepackage{{hyperref}}
\usepackage{{microtype}}
\usepackage{{setspace}}
\usepackage{{fancyhdr}}
\usepackage{{ragged2e}}
\usepackage{{pdflscape}}
\usepackage{{multicol}}
\setlength{{\parindent}}{{0pt}}
\setlength{{\parskip}}{{0.55em}}
\setlength{{\emergencystretch}}{{3em}}
\widowpenalty=10000
\clubpenalty=10000
\fancyhf{{}}
\cfoot{{\thepage}}
\pagestyle{{fancy}}
\hypersetup{{hidelinks}}
"""


def ending() -> str:
    return "\n\\end{document}\n"


def wrap_document(body: str, font_size: str = "12pt", geometry: str = "top=2.5cm,bottom=2.5cm,left=2.5cm,right=2.5cm", header: str | None = None, footer: str | None = None) -> str:
    tex = preamble(font_size, geometry)
    if header:
        tex += f"\\lhead{{{header}}}\n"
    if footer:
        tex += f"\\rfoot{{{footer}}}\n"
    return tex + "\\begin{document}\n" + body.rstrip() + "\n" + ending()
