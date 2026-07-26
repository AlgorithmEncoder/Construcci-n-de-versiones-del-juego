"""
Note editor.
"""

from __future__ import annotations

import pygame

from launcher.widgets.text_editor import TextEditor


class NoteEditor:

    def __init__(self, manager, note):

        self._manager = manager

        self._note = note

        self._editor = TextEditor()

        self._editor.text = note.text

    # --------------------------------------------------

    def draw(self, screen, area):

        self._editor.draw(
            screen,
            area
        )

    # --------------------------------------------------

    def handle_event(self, event):

        changed = self._editor.handle_event(event)

        if changed:

            self._note.text = self._editor.text

            self._manager.flush()

        return changed