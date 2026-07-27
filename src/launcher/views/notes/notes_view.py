"""
Notes workspace.
"""

from __future__ import annotations

import pygame

from launcher.views.notes.toolbar import Toolbar
from launcher.views.notes.breadcrumb import Breadcrumb
from launcher.views.notes.explorer import Explorer
from launcher.views.notes.editor import NoteEditor

from launcher.widgets.input_dialog import InputDialog
from launcher.widgets.move_dialog import MoveDialog


class NotesView:

    def __init__(self, launcher):

        self._launcher = launcher
        self._filesystem = launcher._notes._filesystem

        self._notes = launcher.notes

        self._toolbar = Toolbar()
        self._breadcrumb = Breadcrumb()
        self._explorer = Explorer()

        self._dialog = None
        self._editor = None
        self._selected = None

    # -------------------------------------------------

    def update(self, dt):
        pass

    # -------------------------------------------------

    def draw(self, screen, area):

        toolbar = pygame.Rect(
            area.x + 20,
            area.y + 20,
            area.width - 40,
            40
        )

        breadcrumb = pygame.Rect(
            area.x + 20,
            area.y + 80,
            area.width - 40,
            28
        )

        explorer = pygame.Rect(
            area.x + 20,
            area.y + 120,
            area.width - 40,
            area.height - 140
        )

        self._toolbar.draw(
            screen,
            toolbar
        )

        self._breadcrumb.draw(
            screen,
            breadcrumb,
            self._notes
        )

        if self._editor is not None:

            self._editor.draw(
                screen,
                explorer
            )

        else:

            self._explorer.draw(
                screen,
                explorer,
                self._notes.current,
                self._selected
            )

        if self._dialog is not None:

            self._dialog.draw(screen)

    # -------------------------------------------------

    def handle_event(self, event):

        if self._dialog:

            result = self._dialog.handle_event(event)

            if result:

                self._execute_dialog(result)

            return True

        result = self._toolbar.handle_event(event)
        
        if result:

            self._execute_toolbar(result)

            return True
        
        if self._editor:
        
            return self._editor.handle_event(event)

        result = self._explorer.handle_event(event)

        if result:

            self._execute_explorer(result)

            return True

        return False

    # -------------------------------------------------

    def back(self):
        print("back")

        if self._editor is not None:

            self._editor = None
            self._selected = None

            return True

        if self._filesystem.up():

            self._selected = None

            return True

        return False

    # =================================================
    # Toolbar
    # =================================================

    def _execute_toolbar(self, action):

        if action == "folder":

            self._dialog = InputDialog(
                "Nueva carpeta"
            )

        elif action == "note":

            self._dialog = InputDialog(
                "Nueva nota"
            )

        elif action == "rename":

            if self._selected is None:
                return

            self._dialog = InputDialog(
                "Renombrar"
            )

            self._dialog.value = self._selected.name

        elif action == "delete":

            if self._selected is None:
                return

            self._notes.delete(
                self._selected
            )

            self._selected = None

        elif action == "move":

            if self._selected is None:
                return

            self._dialog = MoveDialog(
                self._filesystem
            )
        
        elif action == "back":
        
            if self.back():

                return True

    # =================================================
    # Dialog
    # =================================================

    def _execute_dialog(self, result):

        action, value = result

        if action == "accept":

            if self._dialog.title == "Nueva carpeta":

                self._notes.create_folder(value)

            elif self._dialog.title == "Nueva nota":

                self._notes.create_note(value)

            elif self._dialog.title == "Renombrar":

                self._notes.rename(
                    self._selected,
                    value
                )

        elif action == "move":

            self._notes.move(
                self._selected,
                value
            )

        self._dialog = None

    # =================================================
    # Explorer
    # =================================================

    def _execute_explorer(self, result):

        action, kind, obj = result

        if action == "select":

            self._selected = obj
            return

        if kind == "folder":

            self._selected = None

            self._notes.enter(obj)

            return

        self._selected = obj

        self._editor = NoteEditor(
            self._notes,
            obj
        )