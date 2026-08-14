"""
Base launcher workspace view.
"""

from __future__ import annotations

import pygame

from launcher import styles


class BaseView:

    # ==================================================
    # Public API
    # ==================================================

    def update(self, dt):
        pass

    # --------------------------------------------------

    def draw(self, screen, area):

        self._draw_background(
            screen,
            area
        )

        self._draw_content(
            screen,
            area
        )

    # --------------------------------------------------

    def handle_event(self, event):

        return False

    # --------------------------------------------------

    def refresh(self):
        pass

    # ==================================================
    # Drawing
    # ==================================================

    def _draw_background(
        self,
        screen,
        area
    ):

        pygame.draw.rect(
            screen,
            styles.WORKSPACE,
            area
        )

    # --------------------------------------------------

    def _draw_content(
        self,
        screen,
        area
    ):
        pass