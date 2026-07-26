"""
Loads and saves the player's notes.
"""

from __future__ import annotations

from pathlib import Path

from launcher.notes.filesystem import FileSystem
from launcher.notes.folder import Folder
from launcher.notes.note import Note

from constants import ROOT_DIR


NOTES_DIR = ROOT_DIR / "assets" / "notes"


class NotesManager:

    def __init__(self):

        self._filesystem = FileSystem()

        NOTES_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.load()

    # ==================================================
    # Properties
    # ==================================================

    @property
    def filesystem(self):

        return self._filesystem

    # ==================================================
    # Loading
    # ==================================================

    def load(self):

        self._filesystem = FileSystem()

        self._load_folder(
            NOTES_DIR,
            self._filesystem.root
        )

    # --------------------------------------------------

    def _load_folder(
        self,
        path: Path,
        folder: Folder
    ):

        for item in sorted(path.iterdir()):

            if item.is_dir():

                child = Folder(item.name)

                folder.add_folder(child)

                self._load_folder(
                    item,
                    child
                )

            elif item.suffix.lower() == ".txt":

                note = Note(
                    name=item.stem,
                    text=item.read_text(
                        encoding="utf-8"
                    )
                )

                folder.add_note(note)

    # ==================================================
    # Saving
    # ==================================================

    def save(self):

        self._clear_directory(NOTES_DIR)

        self._save_folder(
            self._filesystem.root,
            NOTES_DIR
        )

    # --------------------------------------------------

    def _save_folder(
        self,
        folder: Folder,
        path: Path
    ):

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        for note in folder.notes:

            (path / note.filename).write_text(
                note.text,
                encoding="utf-8"
            )

        for child in folder.folders:

            self._save_folder(
                child,
                path / child.name
            )
    
    # --------------------------------------------------
    
    def flush(self):

        self.save()

    # --------------------------------------------------

    def _clear_directory(
        self,
        path: Path
    ):

        if not path.exists():
            return

        for item in path.iterdir():

            if item.is_dir():

                self._clear_directory(item)

                item.rmdir()

            else:

                item.unlink()