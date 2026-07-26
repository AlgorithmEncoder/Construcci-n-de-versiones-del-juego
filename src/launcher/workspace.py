"""
Workspace.

Displays the current view.
"""

from __future__ import annotations

import pygame

from launcher.styles import *


class Workspace:

    def __init__(self):

        self._view = None

    # --------------------------------------------------

    def set_view(self, view):

        self._view = view

    # --------------------------------------------------

    def update(self, dt):

        if self._view:

            self._view.update(dt)

    # --------------------------------------------------

    def draw(self, screen):

        rect = pygame.Rect(

            SIDEBAR_WIDTH,

            HEADER_HEIGHT,

            screen.get_width() - SIDEBAR_WIDTH,

            screen.get_height() - HEADER_HEIGHT - FOOTER_HEIGHT

        )

        pygame.draw.rect(

            screen,

            WORKSPACE,

            rect

        )

        if self._view:

            self._view.draw(

                screen,

                rect

            )

    # --------------------------------------------------

    def handle_event(self, event):

        if self._view:

            return self._view.handle_event(event)

        return False

    # --------------------------------------------------

    @property
    def current(self):

        return self._view