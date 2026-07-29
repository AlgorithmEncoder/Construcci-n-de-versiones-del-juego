"""
document.py

Document overlay.
"""

from __future__ import annotations

import pygame

from constants import (
    WHITE,
    DARK_GREY,
)

from ui.overlay import Overlay
from ui.fonts import Fonts
from ui.text_renderer import draw_wrapped_text


class DocumentUI(Overlay):

    BUTTON_SIZE = 42

    PAPER_MARGIN = 25

    PAPER_COLOR_TOP = (236, 231, 216)
    PAPER_COLOR_BOTTOM = (223, 216, 198)

    PAPER_BORDER = (175, 168, 150)

    TITLE_COLOR = (35, 35, 35)
    TEXT_COLOR = (60, 60, 60)

    DIVIDER_COLOR = (150, 150, 150)

    BUTTON_BG = (55, 55, 55)
    BUTTON_HOVER = (80, 80, 80)
    BUTTON_BORDER = (230, 230, 230)

    SHADOW_ALPHA = 55

    def __init__(
        self,
        document: dict,
        world_width: int,
        world_height: int,
    ):

        super().__init__(
            world_width=world_width,
            world_height=world_height,
            width=900,
            height=550,
        )

        self._document = document

        self._title = document.get("title", "")

        self._pages = (
            document.get("pages")
            or [document.get("text", "")]
        )

        self._page = 0

        self._paper = self.panel.inflate(-50, -50)

        self._create_buttons()

    # ==================================================
    # Events
    # ==================================================

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.close()
                return True

            if event.key == pygame.K_LEFT:

                if self._page > 0:
                    self._page -= 1

                return True

            if event.key == pygame.K_RIGHT:

                if self._page < len(self._pages) - 1:
                    self._page += 1

                return True

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        pos = event.pos

        if (
            self._page > 0
            and self._left_button.collidepoint(pos)
        ):

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
    # Buttons
    # ==================================================

    def _create_buttons(self):

        y = self._paper.bottom - 46

        self._left_button = pygame.Rect(
            self._paper.left + 25,
            y,
            self.BUTTON_SIZE,
            self.BUTTON_SIZE,
        )

        self._right_button = pygame.Rect(
            self._paper.right - 25 - self.BUTTON_SIZE,
            y,
            self.BUTTON_SIZE,
            self.BUTTON_SIZE,
        )

    # ==================================================
    # Draw
    # ==================================================

    def _draw_content(self, screen):

        self._draw_shadow(screen)

        self._draw_paper(screen)

        self._draw_title(screen)

        self._draw_text(screen)

        self._draw_footer(screen)

    # --------------------------------------------------

    def _draw_shadow(self, screen):

        shadow = pygame.Surface(
            (
                self._paper.width + 12,
                self._paper.height + 12,
            ),
            pygame.SRCALPHA,
        )

        pygame.draw.rect(
            shadow,
            (0, 0, 0, self.SHADOW_ALPHA),
            shadow.get_rect(),
            border_radius=8,
        )

        screen.blit(
            shadow,
            (
                self._paper.left + 6,
                self._paper.top + 6,
            ),
        )

    # --------------------------------------------------

    def _draw_paper(self, screen):

        height = self._paper.height

        for i in range(height):

            t = i / height

            color = (

                int(
                    self.PAPER_COLOR_TOP[0] * (1 - t)
                    + self.PAPER_COLOR_BOTTOM[0] * t
                ),

                int(
                    self.PAPER_COLOR_TOP[1] * (1 - t)
                    + self.PAPER_COLOR_BOTTOM[1] * t
                ),

                int(
                    self.PAPER_COLOR_TOP[2] * (1 - t)
                    + self.PAPER_COLOR_BOTTOM[2] * t
                ),
            )

            pygame.draw.line(

                screen,

                color,

                (
                    self._paper.left,
                    self._paper.top + i,
                ),

                (
                    self._paper.right,
                    self._paper.top + i,
                ),
            )

        pygame.draw.rect(

            screen,

            self.PAPER_BORDER,

            self._paper,

            width=2,

            border_radius=6,
        )

    # --------------------------------------------------

    def _draw_title(self, screen):

        title = Fonts.title.render(

            self._title,

            True,

            self.TITLE_COLOR,
        )

        rect = title.get_rect()

        rect.topleft = (
            self._paper.left + 40,
            self._paper.top + 24,
        )

        screen.blit(title, rect)

        y = rect.bottom + 14

        pygame.draw.line(

            screen,

            self.DIVIDER_COLOR,

            (
                self._paper.left + 35,
                y,
            ),

            (
                self._paper.right - 35,
                y,
            ),

            2,
        )

    # --------------------------------------------------

    def _draw_text(self, screen):

        rect = pygame.Rect(

            self._paper.left + 40,

            self._paper.top + 90,

            self._paper.width - 80,

            self._paper.height - 165,
        )

        draw_wrapped_text(

            surface=screen,

            text=self._pages[self._page],

            rect=rect,

            font=Fonts.default,

            color=self.TEXT_COLOR,

            line_spacing=8,

            paragraph_spacing=16,

            preserve_newlines=True,

            title_font=Fonts.subtitle,
        )
    
        # --------------------------------------------------

    def _draw_footer(self, screen):

        total = len(self._pages)

        footer = Fonts.small.render(

            f"Página {self._page + 1} de {total}",

            True,

            self.TEXT_COLOR,
        )

        footer_rect = footer.get_rect()

        footer_rect.center = (

            self._paper.centerx,

            self._paper.bottom - 25,
        )

        screen.blit(
            footer,
            footer_rect,
        )

        if self._page > 0:

            self._draw_button(

                screen,

                self._left_button,

                left=True,
            )

        if self._page < total - 1:

            self._draw_button(

                screen,

                self._right_button,

                left=False,
            )

    # --------------------------------------------------

    def _draw_button(
        self,
        screen,
        rect,
        left: bool,
    ):

        mouse = pygame.mouse.get_pos()

        hovered = rect.collidepoint(mouse)

        bg = (
            self.BUTTON_HOVER
            if hovered
            else self.BUTTON_BG
        )

        pygame.draw.circle(

            screen,

            bg,

            rect.center,

            rect.width // 2,
        )

        pygame.draw.circle(

            screen,

            self.BUTTON_BORDER,

            rect.center,

            rect.width // 2,

            2 if not hovered else 3,
        )

        if left:

            points = [

                (
                    rect.centerx - 5,
                    rect.centery,
                ),

                (
                    rect.centerx + 4,
                    rect.centery - 8,
                ),

                (
                    rect.centerx + 4,
                    rect.centery + 8,
                ),
            ]

        else:

            points = [

                (
                    rect.centerx + 5,
                    rect.centery,
                ),

                (
                    rect.centerx - 4,
                    rect.centery - 8,
                ),

                (
                    rect.centerx - 4,
                    rect.centery + 8,
                ),
            ]

        pygame.draw.polygon(

            screen,

            WHITE,

            points,
        )