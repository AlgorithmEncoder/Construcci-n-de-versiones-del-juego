"""
Reusable multiline text editor.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts
from launcher import styles


class TextEditor:

    PADDING = 16

    def __init__(self):

        self._text = ""

        self._cursor = 0

        self._rect = pygame.Rect(0, 0, 0, 0)
        
        self._focused = False

    # --------------------------------------------------

    @property
    def text(self):

        return self._text

    @text.setter
    def text(self, value):

        self._text = value

        self._cursor = len(value)
    
    @property
    def focused(self):

        return self._focused


    def focus(self):

        self._focused = True


    def blur(self):

        self._focused = False

    # --------------------------------------------------

    def draw(self, screen, rect):

        self._rect = rect

        pygame.draw.rect(
            screen,
            (255,255,255),
            rect
        )

        color = (
            styles.PRIMARY
            if self._focused
            else styles.BORDER
        )

        pygame.draw.rect(
            screen,
            color,
            rect,
            2
        )

        x = rect.x + self.PADDING

        y = rect.y + self.PADDING

        for line in self._text.split("\n"):

            image = Fonts.default.render(
                line,
                True,
                styles.TEXT
            )

            screen.blit(image, (x, y))

            y += image.get_height() + 6

    # --------------------------------------------------

    def handle_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:

            self._focused = self._rect.collidepoint(event.pos)

            return self._focused

        if not self._focused:
            return False

        if event.type != pygame.KEYDOWN:
            return False

        if event.key == pygame.K_BACKSPACE:

            if self._cursor > 0:

                self._text = (
                    self._text[:self._cursor - 1]
                    +
                    self._text[self._cursor:]
                )

                self._cursor -= 1

            return True

        if event.key == pygame.K_RETURN:

            self._text = (
                self._text[:self._cursor]
                +
                "\n"
                +
                self._text[self._cursor:]
            )

            self._cursor += 1

            return True

        if event.key == pygame.K_LEFT:

            self._cursor = max(
                0,
                self._cursor - 1
            )

            return True

        if event.key == pygame.K_RIGHT:

            self._cursor = min(
                len(self._text),
                self._cursor + 1
            )

            return True

        if event.unicode:

            self._text = (
                self._text[:self._cursor]
                +
                event.unicode
                +
                self._text[self._cursor:]
            )

            self._cursor += len(event.unicode)

            return True

        return False