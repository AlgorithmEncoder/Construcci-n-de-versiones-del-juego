"""
Loads and saves the player's notes.
"""

from __future__ import annotations

import shutil

from pathlib import Path

from constants import ROOT_DIR

from launcher.notes.filesystem import FileSystem
from launcher.notes.folder import Folder
from launcher.notes.note import Note


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

    @property
    def root(self):

        return self._filesystem.root

    @property
    def current(self):

        return self._filesystem.current

    @property
    def breadcrumb(self):

        return self._filesystem.breadcrumb

    # ==================================================
    # Navigation
    # ==================================================

    def enter(self, folder):

        self._filesystem.enter(folder)

    # --------------------------------------------------

    def back(self):

        return self._filesystem.back()

    # --------------------------------------------------

    def up(self):

        return self._filesystem.up()

    # ==================================================
    # Loading
    # ==================================================

    def load(self):

        self._filesystem = FileSystem()

        self._load_folder(
            NOTES_DIR,
            self.root
        )

    # --------------------------------------------------

    def _load_folder(
        self,
        path: Path,
        folder: Folder
    ):

        if not path.exists():
            return

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
    # CRUD
    # ==================================================

    def create_folder(self, name):

        name = name.strip()

        if not name:
            return None

        folder = Folder(name)

        self._filesystem.current.add_folder(folder)

        self._path_of(folder).mkdir(
            parents=True,
            exist_ok=True
        )

        return folder

    # --------------------------------------------------

    def create_note(self, name):

        name = name.strip()

        if not name:
            return None

        note = Note(name=name)

        self._filesystem.current.add_note(note)

        self._path_of(note).write_text(
            "",
            encoding="utf-8"
        )

        return note

    # --------------------------------------------------

    def rename(self, item, new_name):

        new_name = new_name.strip()

        if not new_name:

            return False

        old_path = self._path_of(item)

        if isinstance(item, Folder):

            new_path = old_path.parent / new_name

        else:

            new_path = old_path.parent / f"{new_name}.txt"

        old_path.rename(new_path)

        item.name = new_name

        return True

    # --------------------------------------------------

    def delete(self, item):

        path = self._path_of(item)

        if path.exists():

            if isinstance(item, Folder):

                shutil.rmtree(path, onerror=onerror)

            else:

                path.unlink()

        self._filesystem.delete(item)

    # --------------------------------------------------

    def move(self, item, destination):

        if destination is None:

            return False

        old_path = self._path_of(item)

        if isinstance(item, Folder):

            new_path = self._path_of(destination) / item.name

        else:

            new_path = self._path_of(destination) / item.filename

        old_path.rename(new_path)

        self._filesystem.move(
            item,
            destination
        )

        return True

    # ==================================================
    # Utils
    # ==================================================

    def all_folders(self):

        return list(
            self.root.walk()
        )

    # --------------------------------------------------

    def path(self, folder):

        return folder.path
    
    def _path_of(self, item):

        parts = []

        current = item

        while current.parent is not None:

            parts.append(current.name)

            current = current.parent

        parts.reverse()

        path = NOTES_DIR

        for part in parts:

            path /= part

        if isinstance(item, Note):

            path = path.with_suffix(".txt")

        return path
    
    def update_note(self, note):

        self._path_of(note).write_text(
            note.text,
            encoding="utf-8"
        )

def onerror(func, path, exc_info):

    import os
    import stat

    os.chmod(path, stat.S_IWRITE)
    func(path)