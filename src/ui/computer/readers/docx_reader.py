"""
DOCX reader.
"""

from __future__ import annotations

from pathlib import Path

from docx import Document


def read_docx(path: Path) -> str:

    document = Document(path)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:

            paragraphs.append(text)

    return "\n\n".join(paragraphs)