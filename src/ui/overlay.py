"""
overlay.py

Base class for every modal window in the game.
"""

from __future__ import annotations

import pygame

from game import styles


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
        blocks_input: bool = True,
    ):

        self.blocks_input = blocks_input
        self.visible = True

        self._world_width = world_width
        self._world_height = world_height

        # ==================================================
        # Dark overlay background
        # ==================================================

        self._background = pygame.Surface(
            (world_width, world_height),
            pygame.SRCALPHA,
        )

        self._background.fill(
            (
                *styles.OVERLAY_BACKGROUND,
                styles.OVERLAY_BACKGROUND_ALPHA,
            )
        )

        # ==================================================
        # Window panel
        # ==================================================

        self._panel = pygame.Rect(
            0,
            0,
            width,
            height,
        )

        self._panel.center = (
            world_width // 2,
            world_height // 2,
        )

        self._padding = 20

    # ==================================================
    # Public API
    # ==================================================

    def close(self):

        self.visible = False

    # --------------------------------------------------

    def draw(
        self,
        screen: pygame.Surface,
    ):

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
        screen: pygame.Surface,
    ):

        screen.blit(
            self._background,
            (0, 0),
        )

    # --------------------------------------------------

    def _draw_panel(
        self,
        screen: pygame.Surface,
    ):

        pygame.draw.rect(
            screen,
            styles.OVERLAY_PANEL,
            self._panel,
            border_radius=styles.OVERLAY_RADIUS,
        )

        pygame.draw.rect(
            screen,
            styles.OVERLAY_BORDER,
            self._panel,
            width=styles.OVERLAY_BORDER_WIDTH,
            border_radius=styles.OVERLAY_RADIUS,
        )

    # --------------------------------------------------

    def _draw_content(
        self,
        screen: pygame.Surface,
    ):
        """
        Must be implemented by child classes.
        """

        raise NotImplementedError(
            "_draw_content() must be implemented."
        )

    # ==================================================
    # Events
    # ==================================================

    def handle_event(
        self,
        event,
    ) -> bool:
        """
        Returns True if the event was consumed.
        """

        return False

    # ==================================================
    # Update
    # ==================================================

    def update(
        self,
        delta_time: float,
    ):
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

    # --------------------------------------------------

    @property
    def padding(self):

        return self._padding