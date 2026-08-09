from __future__ import annotations

import pygame

from ui.fonts import Fonts
from launcher import styles


class Breadcrumb:

    def draw(self, screen, rect, notes):

        text = Fonts.small.render(
            notes.breadcrumb,
            True,
            styles.TEXT_SECONDARY
        )

        screen.blit(
            text,
            (
                rect.x,
                rect.y
            )
        )