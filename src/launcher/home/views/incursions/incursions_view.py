"""
Incursions list.
"""

from __future__ import annotations

import pygame

from launcher.home.views.incursions.incursion_card import (
    IncursionCard
)

from launcher.base_view import BaseView


class IncursionsView(BaseView):

    CARD_SPACING = 18

    def __init__(
        self,
        launcher
    ):
        self._launcher = launcher
        
        self._language = launcher._language

        self._dreams = launcher.dreams.dreams

        self._cards = []

    # --------------------------------------------------

    def update(
        self,
        dt
    ):
        pass

    # --------------------------------------------------

    def _draw_content(
        self,
        screen,
        area
    ):

        self._cards.clear()

        y = area.y + 25

        width = min(
            700,
            area.width - 40
        )

        for dream in self._dreams:

            rect = pygame.Rect(

                area.x + 20,

                y,

                width,

                IncursionCard.HEIGHT

            )

            card = IncursionCard(self._language)

            card.draw(
                screen,
                rect,
                dream
            )

            self._cards.append(
                (
                    card,
                    dream
                )
            )

            y += (
                IncursionCard.HEIGHT
                +
                self.CARD_SPACING
            )

    # --------------------------------------------------

    def handle_event(
        self,
        event
    ):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        for card, dream in self._cards:

            if card.rect.collidepoint(event.pos):

                return (
                    "open",
                    dream
                )

        return False
    
    
    def refresh(self):
        self._dreams = self._launcher.dreams.dreams