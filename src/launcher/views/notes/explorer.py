"""
Displays folders and notes.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts
from launcher import styles


class Explorer:

    ROW_HEIGHT = 42

    def __init__(self):

        self._rows = []
        self._last_item = None
        self._last_click = 0

    # --------------------------------------------------

    def draw(
            self,
            screen,
            area,
            folder,
            selected=None,
        ):

            self._rows.clear()

            y = area.y + 10

            # ---------------- Folders ----------------

            for child in folder.folders:

                rect = pygame.Rect(
                    area.x + 10,
                    y,
                    area.width - 20,
                    self.ROW_HEIGHT
                )

                selected_item = child is selected

                background = (
                    styles.PRIMARY
                    if selected_item
                    else (245, 245, 245)
                )

                text_color = (
                    styles.TEXT_LIGHT
                    if selected_item
                    else styles.TEXT
                )

                pygame.draw.rect(
                    screen,
                    background,
                    rect,
                    border_radius=6
                )

                pygame.draw.rect(
                    screen,
                    styles.BORDER,
                    rect,
                    1,
                    border_radius=6
                )

                screen.blit(
                    Fonts.default.render(
                        f"📁 {child.name}",
                        True,
                        text_color
                    ),
                    (rect.x + 10, rect.y + 10)
                )

                self._rows.append(
                    ("folder", child, rect)
                )

                y += self.ROW_HEIGHT + 6

            # ---------------- Notes ----------------

            for note in folder.notes:

                rect = pygame.Rect(
                    area.x + 10,
                    y,
                    area.width - 20,
                    self.ROW_HEIGHT
                )

                selected_item = note is selected

                background = (
                    styles.PRIMARY
                    if selected_item
                    else (252, 252, 252)
                )

                text_color = (
                    styles.TEXT_LIGHT
                    if selected_item
                    else styles.TEXT
                )

                pygame.draw.rect(
                    screen,
                    background,
                    rect,
                    border_radius=6
                )

                pygame.draw.rect(
                    screen,
                    styles.BORDER,
                    rect,
                    1,
                    border_radius=6
                )

                screen.blit(
                    Fonts.default.render(
                        f"📄 {note.name}",
                        True,
                        text_color
                    ),
                    (rect.x + 10, rect.y + 10)
                )

                self._rows.append(
                    ("note", note, rect)
                )

                y += self.ROW_HEIGHT + 6

    # --------------------------------------------------

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
                now - self._last_click < 400
            ):

                self._last_item = None

                return ("open", kind, obj)

            self._last_item = obj
            self._last_click = now

            return ("select", kind, obj)

        return None