"""
File explorer.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts

from . import styles
from ui.computer.scroll_view import ScrollView

from pathlib import Path

from icons import (
    get_file_icon,
    draw_folder,
)


class FileList:

    ROW_HEIGHT = 56

    def __init__(self):

        self._rows = []
        self._scroll = None

    # --------------------------------------------------

    def draw(
        self,
        screen,
        area,
        files,
    ):
        if (
            self._scroll is None
            or
            self._scroll.viewport != area
        ):
            self._scroll = ScrollView(area)

        self._scroll.update()

        self._rows.clear()
        
        self._scroll.begin(screen)

        title = Fonts.default
        small = Fonts.small

        y = (
            area.y
            + styles.HEADER_HEIGHT
            + 20
            + self._scroll.y
        )

        for index, file in enumerate(files):

            rect = pygame.Rect(

                area.x + 20,

                y,

                area.width - 40,

                self.ROW_HEIGHT

            )

            pygame.draw.rect(

                screen,

                (248,248,248),

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

            name = file["name"]

            extension = Path(name).suffix.lower()

            icon = (
                get_file_icon(extension)
                if extension
                else draw_folder
            )

            icon_rect = pygame.Rect(
                rect.x + 14,
                rect.y + 16,
                20,
                20,
            )

            icon(
                screen,
                icon_rect,
                styles.TEXT,
            )
            
            screen.blit(

                title.render(

                    name,

                    True,

                    styles.TEXT

                ),

                (
                    rect.x + 44,
                    rect.y + 9
                )

            )

            screen.blit(

                small.render(

                    extension.upper(),

                    True,

                    styles.TEXT_SECONDARY

                ),

                (rect.right - 80, rect.y + 18)

            )

            self._rows.append(

                (rect,index)

            )

            y += self.ROW_HEIGHT + 10
        content_height = (
            y
            - self._scroll.y
            - area.y
        )

        self._scroll.set_content_height(
            content_height
        )

        self._scroll.end(screen)

    # --------------------------------------------------

    def click(self,pos):
        
        pos = self._scroll.translate(pos)

        for rect,index in self._rows:

            if rect.collidepoint(pos):

                return index

        return None
    
    def handle_event(self, event):

        return self._scroll.handle_event(event)