"""
Navigation over the notes tree.
"""

from __future__ import annotations

from launcher.notes.folder import Folder


class FileSystem:

    def __init__(self):

        self._root = Folder("Proyecto")

        self._current = self._root

        self._history = []

    # -------------------------------------------------

    @property
    def root(self):
        return self._root

    @property
    def current(self):
        return self._current

    @property
    def breadcrumb(self):

        return " / ".join(

            self.current.path

        )

    # -------------------------------------------------

    def enter(self, folder):

        self._history.append(self._current)

        self._current = folder

    # -------------------------------------------------

    def back(self):

        if not self._history:
            return False

        self._current = self._history.pop()

        return True

    # -------------------------------------------------

    def up(self):

        if self._current.parent is None:
            return False

        self._current = self._current.parent

        return True
    
    def delete(self, item):

        parent = item.parent

        if parent is None:
            return False

        if isinstance(item, Folder):

            parent.remove_folder(item)

        else:

            parent.remove_note(item)

        return True
    
    def move(self, item, destination):

        if item.parent is None:
            return False

        if destination is item:
            return False

        current = destination

        while current is not None:

            if current is item:
                return False

            current = current.parent

        item.parent.remove_folder(item) if isinstance(item, Folder) else item.parent.remove_note(item)

        if isinstance(item, Folder):

            destination.add_folder(item)

        else:

            destination.add_note(item)

        return True
    
    def all_folders(self):

        return list(self.root.walk())
    
    def get_path(self, folder):

        return folder.path