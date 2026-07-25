"""
computer.py

Computer overlay.
"""

from __future__ import annotations

import pygame

from constants import WHITE

from ui.overlay import Overlay
from ui.fonts import Fonts
from ui.text_renderer import draw_wrapped_text


class ComputerUI(Overlay):

    TABS = (
        "emails",
        "chats",
        "files",
    )

    def __init__(self, computer: dict, world_width: int, world_height: int):

        super().__init__(
            world_width=world_width,
            world_height=world_height,
            width=900,
            height=550
        )

        self._computer = computer

        self._current_tab = "emails"

        self._tab_rects = {}

        self._build_tabs()

    # ==================================================
    # Layout
    # ==================================================

    def _build_tabs(self):

        y = self.panel.top + 70

        for tab in self.TABS:

            rect = pygame.Rect(
                self.panel.left + 20,
                y,
                150,
                40,
            )

            self._tab_rects[tab] = rect

            y += 50

    # ==================================================
    # Events
    # ==================================================

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        for tab, rect in self._tab_rects.items():

            if rect.collidepoint(event.pos):

                self._current_tab = tab

                return True

        return False

    # ==================================================
    # Draw
    # ==================================================

    def _draw_content(self, screen):

        title = Fonts.title.render(
            "Computer",
            True,
            WHITE,
        )

        screen.blit(
            title,
            (
                self.panel.left + 20,
                self.panel.top + 20,
            ),
        )

        self._draw_tabs(screen)

        self._draw_content_area(screen)

    # --------------------------------------------------

    def _draw_tabs(self, screen):

        for tab, rect in self._tab_rects.items():

            color = WHITE

            pygame.draw.rect(
                screen,
                color,
                rect,
                2,
                border_radius=6,
            )

            text = Fonts.default.render(
                tab.capitalize(),
                True,
                color,
            )

            text_rect = text.get_rect(center=rect.center)

            screen.blit(text, text_rect)

    # --------------------------------------------------

    def _draw_content_area(self, screen):

        area = pygame.Rect(

            self.panel.left + 190,

            self.panel.top + 70,

            self.panel.width - 220,

            self.panel.height - 100,
        )

        pygame.draw.rect(
            screen,
            WHITE,
            area,
            2,
        )

        items = self._computer.get(
            self._current_tab,
            [],
        )

        if not items:

            draw_wrapped_text(

                screen,

                "No data.",

                area.inflate(-20, -20),

                Fonts.default,

                WHITE,
            )

            return

        text = "\n".join(
            f"• {item}"
            for item in items
        )

        draw_wrapped_text(

            screen,

            text,

            area.inflate(-20, -20),

            Fonts.default,

            WHITE,
        )