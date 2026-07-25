"""
Conversation list.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts

from . import styles

from ui.computer.scroll_view import ScrollView


class ChatList:

    CARD_HEIGHT = 74

    def __init__(self):

        self._rects = []
        self._scroll = None

    # --------------------------------------------------

    def draw(
        self,
        screen,
        area,
        chats
    ):
        if (
            self._scroll is None
            or
            self._scroll.viewport != area
        ):
            self._scroll = ScrollView(area)

        self._scroll.update()

        self._rects.clear()
        self._scroll.begin(screen)

        title_font = Fonts.default
        small_font = Fonts.small

        y = (
            area.y
            + styles.HEADER_HEIGHT
            + 20
            + self._scroll.y
        )

        for index, chat in enumerate(chats):

            rect = pygame.Rect(
                area.x + 20,
                y,
                area.width - 40,
                self.CARD_HEIGHT
            )

            pygame.draw.rect(
                screen,
                (248,248,248),
                rect,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                styles.BORDER,
                rect,
                1,
                border_radius=8
            )

            screen.blit(
                title_font.render(
                    chat["with"],
                    True,
                    styles.TEXT
                ),
                (rect.x + 14, rect.y + 10)
            )

            preview = ""

            if chat["messages"]:
                preview = chat["messages"][-1]["text"]

            if len(preview) > 45:
                preview = preview[:45] + "..."

            screen.blit(
                small_font.render(
                    preview,
                    True,
                    styles.TEXT_SECONDARY
                ),
                (rect.x + 14, rect.y + 38)
            )

            self._rects.append(
                (rect, index)
            )

            y += self.CARD_HEIGHT + 12
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

        for rect, index in self._rects:

            if rect.collidepoint(pos):
                return index

        return None
    
    def handle_event(self, event):

        return self._scroll.handle_event(event)