"""
Viewer for text-based documents.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts

from ui.computer.scroll_view import ScrollView
from ui.computer import styles

from .base_viewer import BaseViewer


class TextViewer(BaseViewer):

    def __init__(
        self,
        title,
        text,
    ):

        super().__init__(title)

        self._text = text

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

        font = Fonts.default

        y = area.y + 10 + self._scroll.y

        line_height = font.get_height() + 6

        for line in self._text.splitlines():

            surface = font.render(

                line,

                True,

                styles.TEXT

            )

            screen.blit(

                surface,

                (

                    area.x + 10,

                    y

                )

            )

            y += line_height

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