"""
document.py

Document overlay.
"""

from __future__ import annotations

import pygame

from constants import WHITE

from ui.overlay import Overlay
from ui.fonts import Fonts
from ui.text_renderer import draw_wrapped_text


class DocumentUI(Overlay):

    BUTTON_SIZE = 40

    def __init__(self, document: dict, world_width: int, world_height: int):

        super().__init__(
            world_width=world_width,
            world_height=world_height,
            width=900,
            height=550
        )

        self._document = document

        self._title = document.get("title", "")

        self._pages = (
            document.get("pages")
            or [document.get("text", "")]
        )

        self._page = 0

        self._create_buttons()

    # --------------------------------------------------

    def _create_buttons(self):

        y = self.panel.bottom - 55

        self._left_button = pygame.Rect(
            self.panel.left + 25,
            y,
            self.BUTTON_SIZE,
            self.BUTTON_SIZE
        )

        self._right_button = pygame.Rect(
            self.panel.right - 65,
            y,
            self.BUTTON_SIZE,
            self.BUTTON_SIZE
        )

    # ==================================================
    # Events
    # ==================================================

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        pos = event.pos

        if self._page > 0 and self._left_button.collidepoint(pos):
            self._page -= 1
            return True

        if (
            self._page < len(self._pages) - 1
            and self._right_button.collidepoint(pos)
        ):
            self._page += 1
            return True

        return False

    # ==================================================
    # Draw
    # ==================================================

    def _draw_content(self, screen):

        title = Fonts.title.render(
            self._title,
            True,
            WHITE
        )

        screen.blit(
            title,
            (
                self.panel.left + self.padding,
                self.panel.top + self.padding,
            )
        )

        text_rect = pygame.Rect(

            self.panel.left + self.padding,

            self.panel.top + 70,

            self.panel.width - self.padding * 2,

            self.panel.height - 140,
        )

        draw_wrapped_text(

            screen,

            self._pages[self._page],

            text_rect,

            Fonts.default,

            WHITE,
        )

        self._draw_footer(screen)

    # --------------------------------------------------

    def _draw_footer(self, screen):

        total = len(self._pages)

        page = Fonts.default.render(

            f"{self._page + 1}/{total}",

            True,

            WHITE,
        )

        page_rect = page.get_rect()

        page_rect.center = (
            self.panel.centerx,
            self.panel.bottom - 35,
        )

        screen.blit(page, page_rect)

        if self._page > 0:

            pygame.draw.polygon(
                screen,
                WHITE,
                [
                    self._left_button.midleft,
                    self._left_button.topright,
                    self._left_button.bottomright,
                ],
            )

        if self._page < total - 1:

            pygame.draw.polygon(
                screen,
                WHITE,
                [
                    self._right_button.midright,
                    self._right_button.topleft,
                    self._right_button.bottomleft,
                ],
            )