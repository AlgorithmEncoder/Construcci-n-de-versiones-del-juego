from __future__ import annotations

import pygame

from ui.fonts import Fonts
from . import styles


class Header:

    BUTTONS = [
        ("home", "Principal"),
        ("profile", "Perfil"),
        ("settings", "Ajustes"),
    ]

    def __init__(self):

        self.buttons = []

    def draw(self, screen, rect, current):

        pygame.draw.rect(screen, styles.HEADER, rect)

        title = Fonts.title.render(
            "DreamWalker",
            True,
            styles.TEXT_LIGHT
        )

        screen.blit(title, (20, 15))

        self.buttons.clear()

        x = 280

        for key, label in self.BUTTONS:

            r = pygame.Rect(x, 10, 120, 40)

            color = styles.PRIMARY if key == current else (70, 75, 90)

            pygame.draw.rect(screen, color, r, border_radius=6)

            pygame.draw.rect(
                screen,
                styles.TEXT_LIGHT,
                r,
                1,
                border_radius=6
            )

            text = Fonts.default.render(
                label,
                True,
                styles.TEXT_LIGHT
            )

            screen.blit(text, text.get_rect(center=r.center))

            self.buttons.append((r, key))

            x += 130

    def click(self, pos):

        for rect, key in self.buttons:

            if rect.collidepoint(pos):

                return key

        return None