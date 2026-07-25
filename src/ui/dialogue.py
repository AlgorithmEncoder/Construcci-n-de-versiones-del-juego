"""
dialogue.py

Dialogue overlay.

Displays conversations at the bottom of the screen.
"""

from __future__ import annotations

import pygame

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    DARK_GREY,
)

from ui.overlay import Overlay
from ui.fonts import Fonts
from ui.text_renderer import draw_wrapped_text


class DialogueUI(Overlay):
    """
    Bottom dialogue box.

    Left click advances the conversation.
    The last line automatically closes the dialogue.
    """

    def __init__(
        self,
        speaker: str,
        dialogue: list[dict],
        world_width: int,
        world_height: int
    ):

        super().__init__(
            world_width=world_width,
            world_height=world_height,
            width=900,
            height=550
        )

        # Recolocar el panel abajo
        self._panel.midbottom = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 30,
        )

        self._speaker = speaker

        self._dialogue = dialogue

        self._line = 0

    # ==================================================
    # Events
    # ==================================================

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        self._line += 1

        if self._line >= len(self._dialogue):

            self.close()

        return True

    # ==================================================
    # Draw
    # ==================================================

    def _draw_content(
        self,
        screen: pygame.Surface,
    ):

        self._draw_speaker(screen)

        self._draw_text(screen)

        self._draw_continue(screen)

    # --------------------------------------------------

    def _draw_speaker(
        self,
        screen: pygame.Surface,
    ):

        text = Fonts.title.render(
            self._speaker,
            True,
            WHITE,
        )

        screen.blit(
            text,
            (
                self.panel.left + self.padding,
                self.panel.top + self.padding,
            ),
        )

    # --------------------------------------------------

    def _draw_text(
        self,
        screen: pygame.Surface,
    ):

        if self._line >= len(self._dialogue):
            return

        text = self._dialogue[self._line]["text"]

        rect = pygame.Rect(

            self.panel.left + self.padding,

            self.panel.top + 60,

            self.panel.width - self.padding * 2,

            self.panel.height - 90,

        )

        draw_wrapped_text(

            screen,

            text,

            rect,

            Fonts.default,

            WHITE,

        )

    # --------------------------------------------------

    def _draw_continue(
        self,
        screen: pygame.Surface,
    ):

        if self._line >= len(self._dialogue) - 1:
            return

        indicator = Fonts.default.render(
            "▶",
            True,
            WHITE,
        )

        rect = indicator.get_rect()

        rect.bottomright = (

            self.panel.right - self.padding,

            self.panel.bottom - self.padding,

        )

        screen.blit(indicator, rect)