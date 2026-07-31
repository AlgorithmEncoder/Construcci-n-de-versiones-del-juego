"""
Conversation viewer.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts

from . import styles
from ui.computer.scroll_view import ScrollView
from icons import draw_back


class ChatView:

    def __init__(self):

        self._back = pygame.Rect(0, 0, 105, 34)
        self._scroll = None

    # --------------------------------------------------

    def draw(
        self,
        screen,
        area,
        chat
    ):
        if (
            self._scroll is None
            or
            self._scroll.viewport != area
        ):
            self._scroll = ScrollView(area)

        self._scroll.update()

        default = Fonts.default
        small = Fonts.small
        
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

        title = default.render(
            chat["with"],
            True,
            styles.TEXT
        )

        screen.blit(
            title,
            (
                area.x + 130,
                area.y + 18
            )
        )

        y = (
            area.y
            + styles.HEADER_HEIGHT
            + 20
            + self._scroll.y
        )

        max_width = area.width - 80

        for message in chat["messages"]:

            sender = message["sender"]
            text = message["text"]

            bubble = default.render(
                text,
                True,
                styles.TEXT
            )

            padding = 12

            width = min(
                bubble.get_width() + padding * 2,
                max_width
            )

            height = bubble.get_height() + padding * 2

            if sender == chat["with"]:

                rect = pygame.Rect(
                    area.x + 20,
                    y,
                    width,
                    height
                )

                colour = (235,235,235)

            else:

                rect = pygame.Rect(
                    area.right - width - 20,
                    y,
                    width,
                    height
                )

                colour = (205,225,255)

            pygame.draw.rect(
                screen,
                colour,
                rect,
                border_radius=10
            )

            pygame.draw.rect(
                screen,
                styles.BORDER,
                rect,
                1,
                border_radius=10
            )

            screen.blit(
                bubble,
                (
                    rect.x + padding,
                    rect.y + padding
                )
            )

            y += height + 12
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

        return self._back.collidepoint(pos)
    
    def handle_event(self, event):

        return self._scroll.handle_event(event)