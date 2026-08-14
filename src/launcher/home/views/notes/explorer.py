"""
Notes explorer.
"""

from __future__ import annotations

import pygame

from launcher import styles
from ui.fonts import Fonts

from icons import (
    draw_folder,
    draw_note,
)


class Explorer:

    ROW_HEIGHT = 36

    DOUBLE_CLICK_TIME = 350

    def __init__(self):

        self._rows = []

        self._last_item = None

        self._last_click = 0

    # -----------------------------------------------------

    def draw(
        self,
        screen,
        area,
        folder,
        selected=None
    ):

        self._rows.clear()

        pygame.draw.rect(
            screen,
            styles.PANEL,
            area,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            styles.BORDER,
            area,
            1,
            border_radius=8
        )

        y = area.y + 8

        # ---------------- FOLDERS ----------------

        for child in folder.folders:

            rect = pygame.Rect(
                area.x + 8,
                y,
                area.width - 16,
                self.ROW_HEIGHT
            )

            if child is selected:

                color = styles.ROW_SELECTED

            else:

                color = styles.ROW

            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=5
            )

            icon_rect = pygame.Rect(
                rect.x + 10,
                rect.y + 8,
                18,
                18,
            )

            draw_folder(
                screen,
                icon_rect,
                styles.TEXT
            )

            screen.blit(
                Fonts.default.render(
                    child.name,
                    True,
                    styles.TEXT
                ),
                (rect.x + 38, rect.y + 8)
            )

            self._rows.append(

                ("folder", child, rect)

            )

            y += self.ROW_HEIGHT + 4

        # ---------------- NOTES ----------------

        for note in folder.notes:

            rect = pygame.Rect(
                area.x + 8,
                y,
                area.width - 16,
                self.ROW_HEIGHT
            )

            if note is selected:

                color = styles.ROW_SELECTED

            else:

                color = styles.ROW

            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=5
            )

            icon_rect = pygame.Rect(
                rect.x + 10,
                rect.y + 8,
                18,
                18,
            )

            draw_note(
                screen,
                icon_rect,
                styles.TEXT
            )

            screen.blit(
                Fonts.default.render(
                    note.name,
                    True,
                    styles.TEXT
                ),
                (rect.x + 38, rect.y + 8)
            )

            self._rows.append(

                ("note", note, rect)

            )

            y += self.ROW_HEIGHT + 4

    # -----------------------------------------------------

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        now = pygame.time.get_ticks()

        for kind, obj, rect in self._rows:

            if not rect.collidepoint(event.pos):
                continue

            if (

                obj is self._last_item

                and

                now - self._last_click < self.DOUBLE_CLICK_TIME

            ):

                self._last_item = None

                return (
                    "open",
                    kind,
                    obj
                )

            self._last_item = obj

            self._last_click = now

            return (
                "select",
                kind,
                obj
            )

        return None