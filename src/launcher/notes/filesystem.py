"""
In-memory file system.
"""

from __future__ import annotations

from launcher.notes.folder import Folder
from launcher.notes.note import Note


class FileSystem:

    def __init__(self):

        self._root = Folder("Proyecto")

        self._current = self._root

        self._history = []

    # ==================================================
    # Navigation
    # ==================================================

    @property
    def current(self):

        return self._current

    # --------------------------------------------------

    @property
    def root(self):

        return self._root
    
    # --------------------------------------------------
    
    @property
    def breadcrumb(self):

        names = []

        node = self.current

        while node.parent:

            names.append(node.name)

            node = node.parent

        names.append(node.name)

        return " / ".join(reversed(names))

    # --------------------------------------------------

    def enter(self, folder):

        self._history.append(self._current)

        self._current = folder

    # --------------------------------------------------

    def back(self):

        if not self._history:
            return

        self._current = self._history.pop()
    
    # --------------------------------------------------
    
    def up(self):
    
            if self.current.parent:
    
                self.current = self.current.parent

    # ==================================================
    # Creation
    # ==================================================

    def create_folder(self, name: str, parent: Folder | None = None):
        
        name = name.strip()
                
        if not name:
            return False

        parent = parent or self.current

        folder = Folder(name)

        parent.add_folder(folder)

        return folder

    # --------------------------------------------------

    def create_note(self, name: str, parent: Folder | None = None):
        
        name = name.strip()
        
        if not name:
            return False

        parent = parent or self.current

        note = Note(name=name)

        parent.add_note(note)

        return note

    # ==================================================
    # Delete
    # ==================================================

    def delete(self, item):

        parent = item.parent

        if parent is None:
            return

        if isinstance(item, Folder):

            parent.folders.remove(item)

        else:

            parent.notes.remove(item)

    # ==================================================
    # Rename
    # ==================================================

    @staticmethod
    def rename_folder(item, new_name):

        new_name = new_name.strip()

        if not new_name:
            return False
        
        item.name = new_name
        
        return True

    # ==================================================
    # Move
    # ==================================================
    
    def move(self, item, destination: Folder):

        self.delete(item)

        item.parent = destination

        if isinstance(item, Folder):

            destination.add_folder(item)

        else:

            destination.add_note(item)
    
    # ==================================================
    # Utils
    # ==================================================
    
    def get_path(self, item):

        parts = []

        current = item

        while current is not None:

            parts.append(current.name)

            current = current.parent

        return list(reversed(parts))
    
    # --------------------------------------------------
    
    def find_folder(self, path: list[str]):

        folder = self.root

        for name in path:

            folder = next(

                child

                for child in folder.folders

                if child.name == name

            )

        return folder
    
    # --------------------------------------------------
    
    def all_folders(self):

        folders = []

        def walk(folder):

            folders.append(folder)

            for child in folder.folders:

                walk(child)

        walk(self.root)

        return folders