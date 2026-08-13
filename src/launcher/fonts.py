"""
Launcher font manager.

Creates and stores the fonts used by the launcher.
"""

from __future__ import annotations

import pygame

from constants import (
    DEFAULT_FONT,
    DEFAULT_FONT_SIZE,
    TITLE_FONT_SIZE,
    SMALL_FONT_SIZE,
)


class Fonts:

    default = None
    title = None
    small = None

    # ==================================================
    # Initialization
    # ==================================================

    @classmethod
    def initialize(cls):

        cls.default = pygame.font.Font(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE
        )

        cls.title = pygame.font.Font(
            DEFAULT_FONT,
            TITLE_FONT_SIZE
        )

        cls.small = pygame.font.Font(
            DEFAULT_FONT,
            SMALL_FONT_SIZE
        )