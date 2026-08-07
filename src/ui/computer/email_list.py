"""
Inbox view.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts

from . import styles
from ui.computer.scroll_view import ScrollView


class EmailList:

    CARD_HEIGHT = 82

    def __init__(self):

        self._rects = []
        self._scroll = None

    # -------------------------------------------------

    def draw(
        self,
        screen,
        area,
        emails,
    ):

        viewport = pygame.Rect(
            area.x,
            area.y,
            area.width,
            area.height,
        )

        if self._scroll is None:

            self._scroll = ScrollView(
                viewport
            )

        else:

            self._scroll.set_viewport(
                viewport
            )

        self._scroll.update()

        self._rects.clear()

        self._scroll.begin(screen)

        font_title = Fonts.default
        font_small = Fonts.small

        # ==================================================
        # Posición lógica
        # ==================================================

        y = (
            area.y
            + styles.HEADER_HEIGHT
            + 20
        )

        for index, mail in enumerate(emails):

            # ----------------------------------------------
            # Rect lógico
            # ----------------------------------------------

            logical_rect = pygame.Rect(

                area.x + 20,

                y,

                area.width - 40,

                self.CARD_HEIGHT

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
                (248, 248, 248),
                draw_rect,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                styles.BORDER,
                draw_rect,
                1,
                border_radius=8
            )

            # ----------------------------------------------
            # Asunto
            # ----------------------------------------------

            screen.blit(
                font_title.render(
                    mail["subject"],
                    True,
                    styles.TEXT
                ),
                (
                    draw_rect.x + 12,
                    draw_rect.y + 8
                )
            )

            # ----------------------------------------------
            # Remitente
            # ----------------------------------------------

            screen.blit(
                font_small.render(
                    f'De: {mail["from"]}',
                    True,
                    styles.TEXT_SECONDARY
                ),
                (
                    draw_rect.x + 12,
                    draw_rect.y + 34
                )
            )

            # ----------------------------------------------
            # Fecha
            # ----------------------------------------------

            date = font_small.render(
                mail["date"],
                True,
                styles.TEXT_SECONDARY
            )

            screen.blit(
                date,
                (
                    draw_rect.right - date.get_width() - 12,
                    draw_rect.y + 10
                )
            )

            # ----------------------------------------------
            # Guardamos coordenadas lógicas
            # ----------------------------------------------

            self._rects.append(
                (logical_rect, index)
            )

            y += self.CARD_HEIGHT + 12

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

    # -------------------------------------------------

    def click(self,pos):
        
        pos = self._scroll.translate(pos)

        for rect,index in self._rects:

            if rect.collidepoint(pos):

                return index

        return None
    
    def handle_event(self, event):

        return self._scroll.handle_event(event)