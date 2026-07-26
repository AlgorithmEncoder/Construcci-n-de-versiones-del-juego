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
from launcher import styles


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
        self._workspace.update(dt)

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

        handled = self._workspace.handle_event(event)

        view = self._workspace.current

        if isinstance(view, IncursionDetail) or isinstance(view, IncursionsView):
            
            print(self._workspace.current)

            result = self._workspace.handle_event(event)

            if result is None:
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
                print(data)

                self._navigation.push(
                    view
                )

                self._workspace.set_view(
                    IncursionDetail(data)
                )

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