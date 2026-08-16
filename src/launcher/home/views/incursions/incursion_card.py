"""
Single incursion card.
"""

from __future__ import annotations

import pygame

from ui.fonts import Fonts
from launcher import styles


class IncursionCard:

    HEIGHT = 135

    def __init__(self, language_manager):
        
        self._language = language_manager

        self._rect = pygame.Rect(0, 0, 0, 0)

    # --------------------------------------------------

    def draw(
        self,
        screen,
        rect,
        dream
    ):

        self._rect = rect.copy()

        pygame.draw.rect(
            screen,
            styles.CARD,
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

        title = Fonts.title.render(
            dream["title"],
            True,
            styles.TEXT
        )

        screen.blit(
            title,
            (rect.x + 18, rect.y + 14)
        )

        state = (
            self._language.get(
                "launcher",
                "incursions",
                "card",
                "status_locked"
            )
            if dream["locked"]
            else self._language.get(
                "launcher",
                "incursions",
                "card",
                "status_available"
            )
        )

        info = [

            f"{self._language.get(
                'launcher',
                'incursions',
                "card",
                'status'
            )}: {state}",

            f"{self._language.get(
                'launcher',
                'incursions',
                "card",
                'duration'
            )}: {dream['duration']//60} min",

            f"{self._language.get(
                'launcher',
                'incursions',
                "card",
                'iterations'
            )}: {dream['iterations']}",

            f"{self._language.get(
                'launcher',
                'incursions',
                "card",
                'progress'
            )}: {dream['progress']}%"
        ]

        y = rect.y + 50

        for line in info:

            txt = Fonts.default.render(
                line,
                True,
                styles.TEXT_SECONDARY
            )

            screen.blit(
                txt,
                (rect.x + 20, y)
            )

            y += 20

    # --------------------------------------------------

    @property
    def rect(self):

        return self._rect