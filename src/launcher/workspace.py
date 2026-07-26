from __future__ import annotations

import pygame

from ui.fonts import Fonts

from . import styles


class Workspace:

    def draw(self, screen, rect, title):

        pygame.draw.rect(
            screen,
            styles.WORKSPACE,
            rect
        )

        pygame.draw.line(
            screen,
            styles.BORDER,
            (rect.x, rect.y + 55),
            (rect.right, rect.y + 55)
        )

        screen.blit(
            Fonts.title.render(
                title,
                True,
                styles.TEXT
            ),
            (rect.x + 20, rect.y + 16)
        )