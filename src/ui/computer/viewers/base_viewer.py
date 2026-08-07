"""
Base class for every document viewer.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts

from ui.computer import styles
from icons import draw_back


class BaseViewer:

    def __init__(self, title: str):

        self._title = title

        self._back = pygame.Rect(
            0, 0, 110, 36
        )

        self.visible = True

    # ==================================================

    def draw(self, screen, area):

        self._draw_content(
            screen,
            area
        )

    # ==================================================

    def _draw_content(
        self,
        screen,
        area
    ):

        panel = area

        # Fondo blanco
        pygame.draw.rect(
            screen,
            (248, 248, 248),
            panel,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            styles.BORDER,
            panel,
            2,
            border_radius=12
        )

        # ---------------- Header ----------------

        header = pygame.Rect(
            panel.x,
            panel.y,
            panel.width,
            60
        )

        pygame.draw.rect(
            screen,
            styles.PANEL,
            header,
            border_top_left_radius=12,
            border_top_right_radius=12
        )

        screen.blit(
            Fonts.title.render(
                self._title,
                True,
                styles.TEXT
            ),
            (
                panel.x + 24,
                panel.y + 18
            )
        )

        # ---------------- Volver ----------------

        self._back.topright = (
            panel.right - 20,
            panel.y + 12
        )

        pygame.draw.rect(
            screen,
            styles.BUTTON,
            self._back,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            styles.BORDER,
            self._back,
            1,
            border_radius=6
        )

        icon = pygame.Rect(
            self._back.x + 10,
            self._back.y + 9,
            16,
            16
        )

        draw_back(
            screen,
            icon,
            styles.TEXT
        )

        screen.blit(
            Fonts.small.render(
                "Volver",
                True,
                styles.TEXT
            ),
            (
                self._back.x + 34,
                self._back.y + 8
            )
        )

        # ---------------- Área útil ----------------

        content = pygame.Rect(
            panel.x + 20,
            panel.y + 70,
            panel.width - 40,
            panel.height - 90
        )

        previous_clip = screen.get_clip()

        screen.set_clip(content)

        self.draw_document(
            screen,
            content
        )

        screen.set_clip(previous_clip)

    # ==================================================

    def draw_document(
        self,
        screen,
        area
    ):

        raise NotImplementedError

    # ==================================================

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        if self._back.collidepoint(event.pos):

            self.visible = False

            return True

        return False