"""
Reusable input dialog.
"""

from __future__ import annotations

import pygame

from launcher.widgets.text_editor import TextEditor

from launcher import styles
from ui.fonts import Fonts


class InputDialog:

    WIDTH = 420
    HEIGHT = 180

    def __init__(self, title):

        self._title = title

        self._editor = TextEditor()

        self._accept = pygame.Rect(0, 0, 0, 0)

    # -------------------------------------------------

    @property
    def title(self):

        return self._title

    @property
    def value(self):

        return self._editor.text.strip()

    @value.setter
    def value(self, text):

        self._editor.text = text

    # -------------------------------------------------

    def draw(self, screen):

        w = screen.get_width()
        h = screen.get_height()

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill(styles.OVERLAY)
        screen.blit(overlay, (0, 0))

        rect = pygame.Rect(
            (w - self.WIDTH) // 2,
            (h - self.HEIGHT) // 2,
            self.WIDTH,
            self.HEIGHT
        )

        pygame.draw.rect(
            screen,
            styles.DIALOG,
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

        screen.blit(
            Fonts.default.render(
                self._title,
                True,
                styles.TEXT
            ),
            (rect.x + 20, rect.y + 15)
        )

        editor = pygame.Rect(
            rect.x + 20,
            rect.y + 50,
            rect.width - 40,
            44
        )

        self._editor.draw(
            screen,
            editor
        )

        self._accept = pygame.Rect(
            rect.right - 120,
            rect.bottom - 48,
            90,
            30
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
                styles.BUTTON_TEXT
            ),
            (
                self._accept.x + 15,
                self._accept.y + 7
            )
        )

    # -------------------------------------------------

    def handle_event(self, event):

        if self._editor.handle_event(event):
            return None

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