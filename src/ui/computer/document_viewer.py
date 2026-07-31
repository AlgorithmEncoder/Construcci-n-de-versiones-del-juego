"""
document_viewer.py

Creates the appropriate viewer for a document.
"""

from __future__ import annotations

from pathlib import Path

from ui.computer.viewers.text_viewer import TextViewer
from ui.computer.viewers.spreadsheet_viewer import SpreadsheetViewer
from ui.computer.viewers.image_viewer import ImageViewer
from ui.computer.viewers.unsupported_viewer import UnsupportedViewer

# Readers (los iremos creando poco a poco)
from ui.computer.readers.text_reader import read_txt
from ui.computer.readers.docx_reader import read_docx
from ui.computer.readers.pdf_reader import read_pdf
from ui.computer.readers.xlsx_reader import read_xlsx


class DocumentViewer:

    @classmethod
    def create(cls, path: Path):

        extension = path.suffix.lower()

        # ==========================================
        # Text
        # ==========================================

        if extension == ".txt":

            return TextViewer(

                title=path.name,

                text=read_txt(path)

            )

        if extension == ".docx":

            return TextViewer(

                title=path.name,

                text=read_docx(path)

            )

        if extension == ".pdf":

            return TextViewer(

                title=path.name,

                text=read_pdf(path)

            )

        # ==========================================
        # Spreadsheet
        # ==========================================

        if extension == ".xlsx":

            return SpreadsheetViewer(

                title=path.name,

                rows=read_xlsx(path)

            )

        # ==========================================
        # Images
        # ==========================================

        if extension in {

            ".png",

            ".jpg",

            ".jpeg",

            ".bmp",

            ".gif"

        }:

            return ImageViewer(path)

        # ==========================================
        # Unsupported
        # ==========================================

        return UnsupportedViewer(

            title=path.name,

            message="Este tipo de archivo no puede visualizarse."

        )