"""
transition.py

Generic timed transition overlay.

Blocks player input while displaying an optional message.
When the duration finishes, the callback is executed and
the overlay closes automatically.
"""

from __future__ import annotations

from collections.abc import Callable

import pygame

from ui.overlay import Overlay
from ui.fonts import Fonts

from game import styles


class TransitionUI(Overlay):
    """
    Generic transition overlay.

    Examples
    --------
    - Changing room
    - Opening computer
    - Reading document
    - Restarting memory
    - Waiting
    """

    def __init__(
        self,
        world_width: int,
        world_height: int,
        duration: float,
        callback: Callable | None = None,
        text: str | None = None,
    ):

        super().__init__(
            world_width=world_width,
            world_height=world_height,
            width=world_width,
            height=world_height,
            blocks_input=True,
        )

        self._duration = duration
        self._elapsed = 0.0

        self._callback = callback

        self._text = text or ""

        self._dots = 0
        self._dot_timer = 0.0

    # ==================================================
    # Update
    # ==================================================

    def update(
        self,
        delta_time: float,
    ):

        self._elapsed += delta_time

        self._dot_timer += delta_time

        if self._dot_timer >= 0.35:

            self._dot_timer = 0.0
            self._dots = (self._dots + 1) % 4

        if self._elapsed >= self._duration:

            if self._callback is not None:
                self._callback()

            self.close()

    # ==================================================
    # Events
    # ==================================================

    def handle_event(
        self,
        event,
    ) -> bool:
        """
        Consume every input event while the transition
        is active.
        """

        return True

    # ==================================================
    # Drawing
    # ==================================================

    def _draw_panel(
        self,
        screen,
    ):
        """
        No window panel.
        Only the dark background.
        """

        return

    # --------------------------------------------------

    def _draw_content(
        self,
        screen: pygame.Surface,
    ):

        if not self._text:
            return

        message = f"{self._text}{'.' * self._dots}"

        text = Fonts.title.render(
            message,
            True,
            styles.TRANSITION_TEXT,
        )

        rect = text.get_rect(
            center=(
                self.panel.centerx,
                self.panel.centery,
            )
        )

        screen.blit(
            text,
            rect,
        )