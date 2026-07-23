"""
Asset manager.

Loads and caches graphical resources.
"""

from __future__ import annotations

import pygame

from constants import (
    ROOMS_ASSETS_DIR,
    NPC_ASSETS_DIR,
    UI_ASSETS_DIR
)


class Assets:

    _backgrounds = {}
    _sprites = {}
    _icons = {}

    # ==================================================
    # Internal
    # ==================================================

    @classmethod
    def _load_image(cls, path):

        return pygame.image.load(path).convert_alpha()

    # ==================================================
    # Backgrounds
    # ==================================================

    @classmethod
    def get_background(cls, name):

        if name not in cls._backgrounds:

            filepath = ROOMS_ASSETS_DIR / f"{name}.png"

            cls._backgrounds[name] = cls._load_image(filepath)

        return cls._backgrounds[name]

    # ==================================================
    # NPC Sprites
    # ==================================================

    @classmethod
    def get_sprite(cls, name):

        if name not in cls._sprites:

            filepath = NPC_ASSETS_DIR / f"{name}.png"

            cls._sprites[name] = cls._load_image(filepath)

        return cls._sprites[name]

    # ==================================================
    # UI Icons
    # ==================================================

    @classmethod
    def get_icon(cls, name):

        if name not in cls._icons:

            filepath = UI_ASSETS_DIR / f"{name}.png"

            cls._icons[name] = cls._load_image(filepath)

        return cls._icons[name]

    # ==================================================

    @classmethod
    def clear_cache(cls):

        cls._backgrounds.clear()
        cls._sprites.clear()
        cls._icons.clear()