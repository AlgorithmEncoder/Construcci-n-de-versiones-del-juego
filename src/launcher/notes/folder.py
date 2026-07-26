"""
Folder node.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from launcher.notes.note import Note


@dataclass
class Folder:

    name: str

    folders: list["Folder"] = field(default_factory=list)

    notes: list[Note] = field(default_factory=list)

    # --------------------------------------------------

    def folder(self, name):

        for folder in self.folders:

            if folder.name == name:

                return folder

        return None

    # --------------------------------------------------

    def note(self, name):

        for note in self.notes:

            if note.name == name:

                return note

        return None

    # --------------------------------------------------

    def add_folder(self, folder):

        self.folders.append(folder)

    # --------------------------------------------------

    def add_note(self, note):

        self.notes.append(note)

    # --------------------------------------------------

    def remove_folder(self, folder):

        self.folders.remove(folder)

    # --------------------------------------------------

    def remove_note(self, note):

        self.notes.remove(note)