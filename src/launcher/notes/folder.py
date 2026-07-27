"""
Folder node.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from launcher.notes.note import Note


@dataclass
class Folder:

    name: str

    parent: "Folder | None" = None

    folders: list["Folder"] = field(default_factory=list)

    notes: list[Note] = field(default_factory=list)

    # -------------------------------------------------

    @property
    def path(self):

        node = self

        names = []

        while node is not None:

            names.append(node.name)

            node = node.parent

        return list(reversed(names))

    # -------------------------------------------------

    def add_folder(self, folder):

        folder.parent = self

        self.folders.append(folder)

    # -------------------------------------------------

    def add_note(self, note):

        note.parent = self

        self.notes.append(note)

    # -------------------------------------------------

    def remove_folder(self, folder):

        self.folders.remove(folder)

    # -------------------------------------------------

    def remove_note(self, note):

        self.notes.remove(note)

    # -------------------------------------------------

    def walk(self):

        yield self

        for child in self.folders:

            yield from child.walk()

    # -------------------------------------------------

    def descendants(self):

        for child in self.folders:

            yield child

            yield from child.descendants()