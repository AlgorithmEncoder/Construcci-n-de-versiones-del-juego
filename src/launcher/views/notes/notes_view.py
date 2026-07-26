"""
Notes workspace.
"""

from __future__ import annotations

import pygame

from launcher.views.notes.explorer import Explorer
from launcher.views.notes.toolbar import Toolbar
from launcher.views.notes.breadcrumb import Breadcrumb

from launcher.views.notes.editor import NoteEditor
from launcher.widgets.input_dialog import InputDialog


class NotesView:

    def __init__(self, launcher):

        self._launcher = launcher

        self._notes = launcher.notes
        self._filesystem = self._notes.filesystem
        
        self._dialog = None
        self._editor = None
        self._selected = None

        self._toolbar = Toolbar()
        self._breadcrumb = Breadcrumb()
        self._explorer = Explorer()

    def update(self, dt):
        pass

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
            30
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
            self._filesystem
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
                self._filesystem.current,
                self._selected
            )

        if self._dialog is not None:

            self._dialog.draw(screen)

    def handle_event(self, event):
        
        result = self._toolbar.handle_event(event)

        if result:

            if result == "new_folder":

                self._dialog = InputDialog(
                    "Nueva carpeta"
                )

                return True

            if result == "new_note":

                self._dialog = InputDialog(
                    "Nueva nota"
                )

                return True

            if result == "rename":

                if self._selected is not None:

                    self._dialog = InputDialog(
                        "Renombrar"
                    )
                
            if result == "delete":

                if self._selected is not None:

                    self._filesystem.delete(
                        self._selected
                    )

                    self._notes.flush()

                    self._selected = None
                
                if result == "move":

                    ...

            return True
        
        if self._dialog:

            result = self._dialog.handle_event(event)

            if result:

                self._handle_dialog(result)

            return True
        
        if self._editor:

            return self._editor.handle_event(event)
        
        # EXPLORER -------------
        result = self._explorer.handle_event(event)

        if result is None:
            return False

        action, kind, obj = result

        if action == "select":

            self._selected = obj

            return True

        if action == "open":

            if kind == "folder":

                self._selected = None

                self._filesystem.enter(obj)

                return True

            if kind == "note":

                self._selected = obj

                self._editor = NoteEditor(
                    self._notes,
                    obj
                )

                return True

        return False
    
    def back(self):

        if self._editor is not None:

            self._editor = None
            self._selected = None

            return True

        if self._filesystem.current.parent:

            self._filesystem.up()

            return True

        return False
    
    # CREATION -------------
    
    def _create_folder(self, name):

        if self._filesystem.create_folder(name):

            self._notes.flush()
    
    def _create_note(self, name):

        if self._filesystem.create_note(name):

            self._notes.flush()
    
    def _handle_dialog(self, result):

        action, value = result

        if action != "accept":

            return

        if self._dialog.title == "Nueva carpeta":

            self._create_folder(value)

        elif self._dialog.title == "Nueva nota":

            self._create_note(value)

        self._dialog = None