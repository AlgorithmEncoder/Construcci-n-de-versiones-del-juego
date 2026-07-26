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

from launcher.views.incursions.incursions_view import (
    IncursionsView
)
from launcher.views.incursions.incursion_detail import IncursionDetail


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
        
        self._workspace.set_view(

            IncursionsView(self)

        )

        self._module = "home"
        self._section = "incursions"

        self._start_requested = None

    # --------------------------------------------------

    def update(self, dt):
        self._workspace.update(dt)

    # --------------------------------------------------

    def draw(self):

        self._header.draw(
            self._screen,
            self._module
        )

        self._sidebar.draw(
            self._screen,
            self._module,
            self._section
        )

        self._workspace.draw(
            self._screen
        )

        self._footer.draw(
            self._screen
        )

    # --------------------------------------------------

    def handle_event(self, event):

        if self._workspace.handle_event(event):
            return True

        handled = self._workspace.handle_event(event)

        view = self._workspace.current

        if isinstance(view, IncursionDetail):

            result = view.handle_event(event)

            if result:

                action, data = result

                if action == "back":

                    previous = self._navigation.back()

                    if previous:

                        self._workspace.set_view(previous)

                    return True

                if action == "start":

                    self._start_requested = data

                    return True

        return handled

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