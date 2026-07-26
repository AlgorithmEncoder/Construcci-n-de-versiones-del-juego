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

    def draw(self, screen, rect):

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

        if self._view is None:
            return None

        return self._view.handle_event(event)

    # --------------------------------------------------

    @property
    def current(self):

        return self._view