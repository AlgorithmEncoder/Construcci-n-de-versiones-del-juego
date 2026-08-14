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

        # ==================================================
        # Posición lógica
        # ==================================================

        y = (
            area.y
            + styles.HEADER_HEIGHT
            + 20
        )

        for index, file in enumerate(files):

            # ----------------------------------------------
            # Rect lógico
            # ----------------------------------------------

            logical_rect = pygame.Rect(

                area.x + 20,

                y,

                area.width - 40,

                self.ROW_HEIGHT

            )

            # ----------------------------------------------
            # Rect visual
            # ----------------------------------------------

            draw_rect = logical_rect.move(
                0,
                self._scroll.y
            )

            # ----------------------------------------------
            # Fondo
            # ----------------------------------------------

            pygame.draw.rect(

                screen,

                styles.PANEL,

                draw_rect,

                border_radius=6

            )

            pygame.draw.rect(

                screen,

                styles.BORDER,

                draw_rect,

                1,

                border_radius=6

            )

            # ----------------------------------------------
            # Información
            # ----------------------------------------------

            name = file["name"]

            extension = Path(name).suffix.lower()

            icon = (
                get_file_icon(extension)
                if extension
                else draw_folder
            )

            # ----------------------------------------------
            # Icono
            # ----------------------------------------------

            icon_rect = pygame.Rect(

                draw_rect.x + 14,

                draw_rect.y + 16,

                20,

                20

            )

            icon(

                screen,

                icon_rect,

                styles.TEXT,

            )

            # ----------------------------------------------
            # Nombre
            # ----------------------------------------------

            screen.blit(

                title.render(

                    name,

                    True,

                    styles.TEXT

                ),

                (

                    draw_rect.x + 44,

                    draw_rect.y + 9

                )

            )

            # ----------------------------------------------
            # Extensión
            # ----------------------------------------------

            screen.blit(

                small.render(

                    extension.upper(),

                    True,

                    styles.TEXT_SECONDARY

                ),

                (

                    draw_rect.right - 80,

                    draw_rect.y + 18

                )

            )

            # ----------------------------------------------
            # Guardamos posición LÓGICA
            # ----------------------------------------------

            self._rows.append(

                (logical_rect, index)

            )

            # ----------------------------------------------
            # Siguiente elemento
            # ----------------------------------------------

            y += self.ROW_HEIGHT + 10

        # ==================================================
        # Content height
        # ==================================================

        content_height = (
            y
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