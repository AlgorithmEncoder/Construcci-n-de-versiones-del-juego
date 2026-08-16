"""
Creates quick notes from inside the game.

Quick notes are always stored in:

assets/notes/Notas rápidas
"""

from __future__ import annotations

from pathlib import Path

from constants import ASSETS_DIR


NOTES_DIR = ASSETS_DIR / "notes"
QUICK_FOLDER = NOTES_DIR / "Notas rápidas"


def create_quick_note(
    text: str,
    title: str = "New note"
) -> Path:

    """
    Creates a quick note.

    If a note with the same title already exists,
    a numeric suffix is added:

    Nueva nota.txt
    Nueva nota (1).txt
    Nueva nota (2).txt
    """

    QUICK_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = _next_filename(title)

    path = QUICK_FOLDER / filename

    path.write_text(
        text,
        encoding="utf-8"
    )

    return path


# --------------------------------------------------


def _next_filename(title: str) -> str:

    title = title.strip()

    if not title:

        title = "New note"

    candidate = f"{title}.txt"

    if not (QUICK_FOLDER / candidate).exists():

        return candidate

    index = 1

    while True:

        candidate = f"{title} ({index}).txt"

        if not (QUICK_FOLDER / candidate).exists():

            return candidate

        index += 1