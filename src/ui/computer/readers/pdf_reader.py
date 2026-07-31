"""
PDF reader.
"""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


def read_pdf(path: Path) -> str:

    reader = PdfReader(path)

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:

            pages.append(text)

    return "\n\n".join(pages)