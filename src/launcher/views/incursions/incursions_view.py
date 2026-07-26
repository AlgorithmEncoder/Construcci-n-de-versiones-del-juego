"""
Incursions list.
"""

from __future__ import annotations

import pygame

from launcher.views.incursions.incursion_card import (
    IncursionCard
)
from launcher.views.incursions.incursion_detail import IncursionDetail


class IncursionsView:

    CARD_SPACING = 18

    def __init__(
        self,
        launcher
    ):
        self.launcher = launcher

        self._dreams = launcher.dreams.dreams

        self._cards = []

    # --------------------------------------------------

    def update(
        self,
        dt
    ):
        pass

    # --------------------------------------------------

    def draw(
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

            card = IncursionCard()

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

                self._launcher.navigation.push(self)

                self._launcher.workspace.set_view(

                    IncursionDetail(dream)

                )

                return True

        return False