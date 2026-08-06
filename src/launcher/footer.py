from __future__ import annotations

import pygame

from ui.fonts import Fonts

from . import styles

from constants import GAME_VERSION


class Footer:

    def __init__(self):

        self.message = "Sistema preparado."

    def draw(self, screen, rect):

        pygame.draw.rect(
            screen,
            styles.FOOTER,
            rect
        )

        version = Fonts.small.render(
            GAME_VERSION,
            True,
            styles.TEXT_LIGHT
        )

        author = Fonts.small.render(
            "© Ferran Clausell",
            True,
            styles.TEXT_LIGHT
        )

        msg = Fonts.small.render(
            self.message,
            True,
            styles.TEXT_LIGHT
        )

        screen.blit(version, (15, rect.y + 6))

        screen.blit(msg, (150, rect.y + 6))

        screen.blit(
            author,
            (
                rect.right - author.get_width() - 15,
                rect.y + 6
            )
        )