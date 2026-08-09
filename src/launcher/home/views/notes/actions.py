"""
Actions used by NotesView.
"""

from enum import Enum


class NotesAction(Enum):

    CREATE_FOLDER = "folder"

    CREATE_NOTE = "note"

    RENAME = "rename"

    DELETE = "delete"

    MOVE = "move"

    SELECT = "select"

    OPEN = "open"

    BACK = "back"