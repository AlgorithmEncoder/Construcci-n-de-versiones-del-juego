"""
overlay.py

Base class for every modal window in the game.
"""

from __future__ import annotations

import pygame

from constants import (
    DARK_GREY,
    WHITE
)


class Overlay:
    """
    Base modal window.

    Every UI window (computer, document, dialogue...)
    inherits from this class.
    """

    def __init__(
        self,
        world_width: int,
        world_height: int,
        width: int = 900,
        height: int = 550,
        blocks_input: bool = True
    ):

        self.blocks_input = blocks_input
        self.visible = True

        self._world_width = world_width
        self._world_height = world_height

        # Capa oscura semitransparente
        self._background = pygame.Surface(
            (world_width, world_height),
            pygame.SRCALPHA
        )
        self._background.fill((0, 0, 0, 160))

        # Ventana
        self._panel = pygame.Rect(
            0,
            0,
            width,
            height
        )

        self._panel.center = (
            world_width // 2,
            world_height // 2
        )

        self._padding = 20

    # ==================================================
    # Public API
    # ==================================================

    def close(self):

        self.visible = False

    def draw(self, screen: pygame.Surface):

        if not self.visible:
            return

        self._draw_background(screen)

        self._draw_panel(screen)

        self._draw_content(screen)

    # ==================================================
    # Draw
    # ==================================================

    def _draw_background(
        self,
        screen: pygame.Surface
    ):

        screen.blit(self._background, (0, 0))

    # --------------------------------------------------

    def _draw_panel(
        self,
        screen: pygame.Surface
    ):

        pygame.draw.rect(
            screen,
            DARK_GREY,
            self._panel,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            WHITE,
            self._panel,
            width=2,
            border_radius=12
        )

    # --------------------------------------------------

    def _draw_content(
        self,
        screen: pygame.Surface
    ):
        """
        Must be implemented by child classes.
        """
        raise NotImplementedError(
            "_draw_content() must be implemented."
        )
    
    def handle_event(self, event) -> bool:
        """
        Devuelve True si el evento ha sido consumido.
        """
        return False
    
    def update(self, delta_time: float):
        """
        Optional update.
        """
        pass

    # ==================================================
    # Properties
    # ==================================================

    @property
    def panel(self):

        return self._panel

    @property
    def padding(self):

        return self._padding