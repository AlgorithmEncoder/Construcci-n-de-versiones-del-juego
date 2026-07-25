"""
Reusable scrollable viewport.
"""

from __future__ import annotations

import pygame

class ScrollView:

    WHEEL_STEP = 70
    SMOOTHING = 0.22

    def __init__(self, viewport: pygame.Rect):

        self.viewport = viewport

        self.offset = 0.0
        self.target = 0.0

        self.content_height = 0

    # ==================================================
    # Public API
    # ==================================================

    def begin(self, screen: pygame.Surface):

        screen.set_clip(self.viewport)

    def end(self, screen: pygame.Surface):

        screen.set_clip(None)

    # --------------------------------------------------

    def update(self):

        self.offset += (
            self.target - self.offset
        ) * self.SMOOTHING

    # --------------------------------------------------

    def set_content_height(
        self,
        height: int
    ):

        self.content_height = max(
            height,
            self.viewport.height
        )

        self._clamp()

    # --------------------------------------------------

    def handle_event(self, event) -> bool:

        if event.type != pygame.MOUSEWHEEL:
            return False

        mouse = pygame.mouse.get_pos()

        if not self.viewport.collidepoint(mouse):
            return False

        self.target -= (
            event.y * self.WHEEL_STEP
        )

        self._clamp()

        return True

    # --------------------------------------------------

    def translate(
        self,
        position: tuple[int, int]
    ) -> tuple[int, int]:

        return (
            position[0],
            position[1] + int(self.offset)
        )

    # --------------------------------------------------

    @property
    def y(self):

        return -int(self.offset)

    # ==================================================
    # Internal
    # ==================================================

    def _clamp(self):

        maximum = max(
            0,
            self.content_height - self.viewport.height
        )

        self.target = max(
            0,
            min(
                self.target,
                maximum
            )
        )