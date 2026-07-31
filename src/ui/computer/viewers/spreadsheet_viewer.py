"""
Viewer for Excel spreadsheets.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts
from ui.computer.scroll_view import ScrollView
from ui.computer import styles

from .base_viewer import BaseViewer


class SpreadsheetViewer(BaseViewer):

    CELL_WIDTH = 170
    ROW_HEIGHT = 30

    def __init__(
        self,
        title,
        rows,
    ):

        super().__init__(title)

        self._rows = rows

        self._scroll = None

    # ==================================================

    def draw_document(
        self,
        screen,
        area,
    ):

        if (
            self._scroll is None
            or
            self._scroll.viewport != area
        ):

            self._scroll = ScrollView(area)

        self._scroll.update()

        self._scroll.begin(screen)

        font = Fonts.small

        y = area.y + 10 + self._scroll.y

        for row in self._rows:

            x = area.x + 10

            for value in row:

                rect = pygame.Rect(

                    x,
                    y,
                    self.CELL_WIDTH,
                    self.ROW_HEIGHT

                )

                pygame.draw.rect(

                    screen,

                    (255,255,255),

                    rect

                )

                pygame.draw.rect(

                    screen,

                    styles.BORDER,

                    rect,

                    1

                )

                screen.blit(

                    font.render(

                        value,

                        True,

                        styles.TEXT

                    ),

                    (

                        rect.x + 6,

                        rect.y + 7

                    )

                )

                x += self.CELL_WIDTH

            y += self.ROW_HEIGHT

        self._scroll.set_content_height(

            y - self._scroll.y - area.y

        )

        self._scroll.end(screen)

    # ==================================================

    def handle_event(self, event):

        if super().handle_event(event):
            return True

        if self._scroll:
            return self._scroll.handle_event(event)

        return False