"""
Main launcher window.
"""

from __future__ import annotations

import pygame

from launcher.header import Header
from launcher.sidebar import Sidebar
from launcher.workspace import Workspace
from launcher.footer import Footer

from launcher.navigation import Navigation
from launcher.dream_manager import DreamManager

from launcher.widgets.empty_view import EmptyView

from launcher.views.incursions.incursions_view import (
    IncursionsView
)
from launcher.views.incursions.incursion_detail import IncursionDetail
from launcher import styles

from launcher.notes.notes_manager import NotesManager
from launcher.views.notes.notes_view import NotesView


class MainWindow:

    def __init__(self, screen: pygame.Surface):

        self._screen = screen
        
        self._start_requested = None
        self._running = True

        self._header = Header()
        self._sidebar = Sidebar()
        self._workspace = Workspace()
        self._footer = Footer()

        self._navigation = Navigation()

        self._dreams = DreamManager()
        self._dreams.load()
        self._notes = NotesManager()
        self._notes_view = NotesView(self)
        
        self._sections = {
            "incursions": IncursionsView(self),
            "notes": self._notes_view,
            "inventory": EmptyView(),
            "stats": EmptyView(),
            "achievements": EmptyView(),
            "activity": EmptyView(),
            "general": EmptyView(),
            "audio": EmptyView(),
            "display": EmptyView(),
            "language": EmptyView(),
        }
        
        self._workspace.set_view(
            self._sections["incursions"]
        )

        self._module = "home"
        self._section = "incursions"

        self._start_requested = None
        
        self._header_rect = pygame.Rect(
            0,
            0,
            self._screen.get_width(),
            styles.HEADER_HEIGHT
        )

        self._footer_rect = pygame.Rect(
            0,
            self._screen.get_height() - styles.FOOTER_HEIGHT,
            self._screen.get_width(),
            styles.FOOTER_HEIGHT
        )

        self._sidebar_rect = pygame.Rect(
            0,
            styles.HEADER_HEIGHT,
            styles.SIDEBAR_WIDTH,
            self._screen.get_height() - styles.HEADER_HEIGHT - styles.FOOTER_HEIGHT
        )

        self._workspace_rect = pygame.Rect(
            styles.SIDEBAR_WIDTH,
            styles.HEADER_HEIGHT,
            self._screen.get_width() - styles.SIDEBAR_WIDTH,
            self._screen.get_height() - styles.HEADER_HEIGHT - styles.FOOTER_HEIGHT
        )

    # --------------------------------------------------

    def update(self, dt):
        
        if self._workspace.current:

            self._workspace.current.update(dt)

    # --------------------------------------------------

    def draw(self):

        self._header.draw(
            self._screen,
            self._header_rect,
            self._module
        )

        self._sidebar.draw(
            self._screen,
            self._sidebar_rect,
            self._module,
            self._section
        )

        self._workspace.draw(
            self._screen,
            self._workspace_rect
        )

        self._footer.draw(
            self._screen,
            self._footer_rect
        )

    # --------------------------------------------------

    def handle_event(self, event):
        
        # HEADER ------------
        module = self._header.handle_event(event)

        if module:

            self._change_module(module)

            return True
        
        # SIDEBAR ----------------
        section = self._sidebar.handle_event(event)

        if section:

            self._change_section(section)

            return True
        
        # CONTENT -------------

        handled = self._workspace.handle_event(event)

        view = self._workspace.current

        if isinstance(view, IncursionDetail) or isinstance(view, IncursionsView):

            result = handled

            if result is None or result is False:
                return False

            if result == True:
                return True

            action, data = result

            if action == "back":

                previous = self._navigation.back()

                if previous:

                    self._workspace.set_view(previous)

                return True

            if action == "start":

                self._start_requested = data

                return True
            
            if action == "open":

                self._navigation.push(
                    view
                )

                self._workspace.set_view(
                    IncursionDetail(
                        self._dreams,
                        data["id"]
                    )
                )
        
        elif isinstance(view, NotesView):

            result = handled

            if result is None:
                return False

        return handled
    
    def _change_section(self, section):

        valid_sections = {
            key
            for key, _ in self._sidebar.MODULES[self._module]
        }

        if section not in valid_sections:
            return False

        view = self._sections.get(section)

        if view is None:
            return False

        self._section = section
        self._workspace.set_view(view)

        return True
    
    def _change_module(self, module):

        if not self._sidebar.set_module(module):
            return False

        self._module = module
        self._sidebar.update(self._sidebar_rect)

        first_section = self._sidebar.MODULES[module][0][0]
        self._change_section(first_section)
        
        return True

    # ==================================================

    @property
    def start_requested(self):
        return self._start_requested

    @property
    def running(self):
        return self._running
    
    @property
    def dreams(self):
        return self._dreams
    
    @property
    def notes(self):

        return self._notes

    @property
    def navigation(self):
        return self._navigation

    @property
    def workspace(self):
        return self._workspace

    @property
    def start_requested(self):
        return self._start_requested

    # --------------------------------------------------

    def start_memory(self, memory):

        self._start_requested = memory
    
    def clear_requests(self):

        self._start_requested = None
    
    def refresh(self):
        
        self._dreams.load()
        
        # Refresh views
        for view in self._sections.values():
            
            if hasattr(view, "refresh"):

                view.refresh()
        
        current_view = self._workspace.current
        if hasattr(current_view, "refresh"):
            current_view.refresh()