"""
Opened email.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts

from . import styles
from ui.computer.scroll_view import ScrollView
from icons import draw_back


class EmailView:

    def __init__(self):

        self._back = pygame.Rect(0, 0, 105, 34)
        self._scroll = None

    # -------------------------------------------------

    def draw(
        self,
        screen,
        area,
        email
    ):
        if (
            self._scroll is None
            or
            self._scroll.viewport != area
        ):
            self._scroll = ScrollView(area)

        self._scroll.update()

        font = Fonts.default
        small = Fonts.small
        
        self._scroll.begin(screen)

        self._back.topleft = (
            area.x+600,
            area.y+15
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
            self._back.y + 9,
            14,
            14,
        )

        draw_back(
            screen,
            icon_rect,
            styles.TEXT
        )

        text = small.render(
            "Volver",
            True,
            styles.TEXT
        )

        screen.blit(
            text,
            (
                self._back.x + 30,
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
            font.render(
                email["subject"],
                True,
                styles.TEXT
            ),
            (area.x+20,y)
        )

        y += 40

        screen.blit(
            small.render(
                f'De: {email["from"]}',
                True,
                styles.TEXT_SECONDARY
            ),
            (area.x+20,y)
        )

        y += 24

        screen.blit(
            small.render(
                f'Para: {email["to"]}',
                True,
                styles.TEXT_SECONDARY
            ),
            (area.x+20,y)
        )

        y += 24

        screen.blit(
            small.render(
                email["date"],
                True,
                styles.TEXT_SECONDARY
            ),
            (area.x+20,y)
        )

        y += 45

        for line in email["body"]:

            text = font.render(
                line,
                True,
                styles.TEXT
            )

            screen.blit(
                text,
                (area.x+20,y)
            )

            y += 28
        content_height = (
            y
            - self._scroll.y
            - area.y
        )

        self._scroll.set_content_height(
            content_height
        )

        self._scroll.end(screen)

    # -------------------------------------------------

    def click(self,pos):
        
        pos = self._scroll.translate(pos)

        return self._back.collidepoint(pos)
    
    def handle_event(self, event):

        return self._scroll.handle_event(event)