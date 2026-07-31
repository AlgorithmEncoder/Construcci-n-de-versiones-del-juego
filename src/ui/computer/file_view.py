"""
Selected file.
"""

from __future__ import annotations

import pygame
from pathlib import Path

from ui.fonts import Fonts

from . import styles
from ui.computer.scroll_view import ScrollView
from icons import draw_back

from managers.computer_files_manager import ComputerFilesManager


class FileView:

    def __init__(self):

        self._back = pygame.Rect(0, 0, 105, 34)

        self._open = pygame.Rect(0,0,120,40)
        
        self._scroll = None

    # --------------------------------------------------

    def draw(
        self,
        screen,
        area,
        file
    ):
        if (
            self._scroll is None
            or
            self._scroll.viewport != area
        ):
            self._scroll = ScrollView(area)

        self._scroll.update()

        title = Fonts.title

        default = Fonts.default

        small = Fonts.small
        files = ComputerFilesManager()
        info = files.info(
            file["document_id"]
        )

        self._file_exists = info["exists"]
        
        self._scroll.begin(screen)

        self._back.topleft = (

            area.x + 600,

            area.y + 15

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

        icon_rect = pygame.Rect(
            self._back.x + 10,
            self._back.y + 8,
            16,
            16,
        )

        draw_back(
            screen,
            icon_rect,
            styles.TEXT,
        )
        
        screen.blit(

            small.render(

                "Volver",

                True,

                styles.TEXT

            ),

            (
                self._back.x + 32,
                self._back.y + 8
            )

        )

        y = (
            area.y
            + styles.HEADER_HEIGHT
            + 20
            + self._scroll.y
        )

        screen.blit(

            title.render(

                file["name"],

                True,

                styles.TEXT

            ),

            (area.x + 30, y)

        )

        y += 60

        screen.blit(

            default.render(

                f'Document ID: {file["document_id"]}',

                True,

                styles.TEXT_SECONDARY

            ),

            (area.x + 30, y)

        )

        y += 60

        pygame.draw.rect(

            screen,

            (210,210,210),

            self._open,

            border_radius=8

        )

        self._open.topleft = (

            area.x + 30,

            y

        )

        pygame.draw.rect(

            screen,

            styles.BORDER,

            self._open,

            1,

            border_radius=8

        )

        screen.blit(

            default.render(

                "Abrir",

                True,

                (140,140,140)

            ),

            (

                self._open.x + 28,

                self._open.y + 10

            )

        )
        print()

        screen.blit(

            small.render(

                "(Disponible próximamente)",

                True,

                styles.TEXT_SECONDARY

            ),

            (

                area.x + 180,

                y + 12

            )

        )
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

    def click(self, pos):

        pos = self._scroll.translate(pos)

        if self._back.collidepoint(pos):
            return "back"

        if (
            self._file_exists
            and
            self._open.collidepoint(pos)
        ):
            return "open"

        return None
    
    def handle_event(self, event):

        return self._scroll.handle_event(event)