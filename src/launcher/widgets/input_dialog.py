"""
Reusable input dialog.
"""

from __future__ import annotations

import pygame

from launcher.widgets.text_editor import TextEditor

from ui.fonts import Fonts
from launcher import styles


class InputDialog:

    WIDTH = 420

    HEIGHT = 180

    def __init__(self, title):

        self._title = title

        self._editor = TextEditor()

        self._accept = pygame.Rect()

    # --------------------------------------------------

    @property
    def value(self):

        return self._editor.text.strip()
    
    @property
    def title(self):

        return self._title

    # --------------------------------------------------

    def draw(self, screen):

        w = screen.get_width()

        h = screen.get_height()

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)

        overlay.fill((0,0,0,120))

        screen.blit(overlay, (0,0))

        rect = pygame.Rect(
            (w-self.WIDTH)//2,
            (h-self.HEIGHT)//2,
            self.WIDTH,
            self.HEIGHT
        )

        pygame.draw.rect(
            screen,
            (250,250,250),
            rect,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            styles.BORDER,
            rect,
            2,
            border_radius=8
        )

        title = Fonts.default.render(
            self._title,
            True,
            styles.TEXT
        )

        screen.blit(
            title,
            (rect.x+20, rect.y+15)
        )

        editor = pygame.Rect(
            rect.x+20,
            rect.y+50,
            rect.width-40,
            45
        )

        self._editor.draw(
            screen,
            editor
        )

        self._accept = pygame.Rect(
            rect.right-120,
            rect.bottom-50,
            90,
            32
        )

        pygame.draw.rect(
            screen,
            styles.PRIMARY,
            self._accept,
            border_radius=5
        )

        screen.blit(
            Fonts.small.render(
                "Aceptar",
                True,
                (255,255,255)
            ),
            (
                self._accept.x+15,
                self._accept.y+8
            )
        )

    # --------------------------------------------------

    def handle_event(self, event):

        self._editor.handle_event(event)

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        if self._accept.collidepoint(event.pos):

            return (
                "accept",
                self.value
            )

        return None