"""
Font manager.
"""

from __future__ import annotations

import pygame

from constants import (
    DEFAULT_FONT,
    DEFAULT_FONT_SIZE,
    TITLE_FONT_SIZE,
    SMALL_FONT_SIZE
)


class Fonts:

    title = None
    default = None
    small = None

    @classmethod
    def initialize(cls, scale=1.0):

        cls.title = pygame.font.Font(
            DEFAULT_FONT,
            int(TITLE_FONT_SIZE*scale)
        )

        cls.default = pygame.font.Font(
            DEFAULT_FONT,
            int(DEFAULT_FONT_SIZE*scale)
        )

        cls.small = pygame.font.Font(
            DEFAULT_FONT,
            int(SMALL_FONT_SIZE*scale)
        )
        
        cls.clock = pygame.font.Font(None, int(44*scale))
        
        cls.subtitle = pygame.font.Font(
            DEFAULT_FONT,
            int((DEFAULT_FONT_SIZE + 4)*scale)
        )