"""
computer_files_manager.py

Maps document IDs to real files stored in assets/computer_files.
"""

from __future__ import annotations

import json
import os

from pathlib import Path

from managers.path_manager import PathManager


class ComputerFilesManager:

    def __init__(self):

        with open(
            PathManager.json_folder() / "computer_files.json",
            "r",
            encoding="utf-8"
        ) as f:

            self._documents = json.load(f)

    # ==================================================
    # Public API
    # ==================================================

    def exists(self, document_id: str) -> bool:

        return self.path(document_id) is not None

    # --------------------------------------------------

    def path(self, document_id: str) -> Path | None:

        info = self._documents.get(document_id)

        if info is None:
            return None

        path = PathManager.documents() / info["file"]

        if not path.exists():
            return None

        return path

    # --------------------------------------------------

    def open(self, document_id: str) -> bool:

        path = self.path(document_id)

        if path is None:
            return False

        os.startfile(path)

        return True

    # --------------------------------------------------

    def info(self, document_id: str) -> dict | None:

        info = self._documents.get(document_id)

        if info is None:
            return None

        path = PathManager.documents() / info["file"]

        return {

            "document_id": document_id,

            "path": path,

            "exists": path.exists(),

            "extension": path.suffix.lower(),

            "filename": path.name

        }