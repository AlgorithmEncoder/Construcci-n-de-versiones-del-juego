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
    def initialize(cls):

        cls.title = pygame.font.Font(
            DEFAULT_FONT,
            TITLE_FONT_SIZE
        )

        cls.default = pygame.font.Font(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE
        )

        cls.small = pygame.font.Font(
            DEFAULT_FONT,
            SMALL_FONT_SIZE
        )
        
        cls.clock = pygame.font.Font(None, 44)
        
        cls.subtitle = pygame.font.Font(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE + 4
        )