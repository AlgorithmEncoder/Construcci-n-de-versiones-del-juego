"""
Folder selection dialog.
"""

from __future__ import annotations

import pygame

from launcher import styles
from ui.fonts import Fonts


class MoveDialog:

    WIDTH = 500
    HEIGHT = 420

    ROW_HEIGHT = 34

    def __init__(self, filesystem):

        self._filesystem = filesystem

        self._selected = filesystem.current

        self._rows = []

        self._accept = pygame.Rect(0, 0, 0, 0)

    # -----------------------------------------------------

    @property
    def destination(self):

        return self._selected

    # -----------------------------------------------------

    def draw(self, screen):

        w = screen.get_width()
        h = screen.get_height()

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill(styles.OVERLAY)

        screen.blit(overlay, (0, 0))

        rect = pygame.Rect(
            (w - self.WIDTH) // 2,
            (h - self.HEIGHT) // 2,
            self.WIDTH,
            self.HEIGHT
        )

        pygame.draw.rect(
            screen,
            styles.DIALOG,
            rect,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            styles.BORDER,
            rect,
            2,
            border_radius=8
        )

        screen.blit(

            Fonts.default.render(

                "Mover a...",

                True,

                styles.TEXT

            ),

            (rect.x + 20, rect.y + 15)

        )

        self._rows.clear()

        y = rect.y + 60

        for folder in self._filesystem.all_folders():

            row = pygame.Rect(
                rect.x + 20,
                y,
                rect.width - 40,
                self.ROW_HEIGHT
            )

            selected = folder is self._selected

            pygame.draw.rect(
                screen,
                styles.PRIMARY if selected else styles.ROW,
                row,
                border_radius=5
            )

            pygame.draw.rect(
                screen,
                styles.BORDER,
                row,
                1,
                border_radius=5
            )

            path = "/".join(
                self._filesystem.get_path(folder)
            )

            color = (
                styles.TEXT_LIGHT
                if selected
                else styles.TEXT
            )

            screen.blit(
                Fonts.small.render(
                    path,
                    True,
                    color
                ),
                (row.x + 10, row.y + 8)
            )

            self._rows.append(
                (folder, row)
            )

            y += self.ROW_HEIGHT + 6

        self._accept = pygame.Rect(
            rect.right - 110,
            rect.bottom - 45,
            90,
            30
        )

        pygame.draw.rect(
            screen,
            styles.PRIMARY,
            self._accept,
            border_radius=5
        )

        screen.blit(
            Fonts.small.render(
                "Mover",
                True,
                styles.BUTTON_TEXT
            ),
            (self._accept.x + 18, self._accept.y + 7)
        )

    # -----------------------------------------------------

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        for folder, rect in self._rows:

            if rect.collidepoint(event.pos):

                self._selected = folder

                return None

        if self._accept.collidepoint(event.pos):

            return (
                "move",
                self._selected
            )

        return None