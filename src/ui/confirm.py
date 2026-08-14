"""
confirm.py

Confirmation modal window.
"""

from __future__ import annotations

import pygame

from ui.overlay import Overlay
from ui.fonts import Fonts

from game import styles


class ConfirmUI(Overlay):

    def __init__(
        self,
        title: str,
        message: str,
        on_confirm,
        world_width: int,
        world_height: int,
    ):

        super().__init__(
            world_width=world_width,
            world_height=world_height,
            width=600,
            height=280,
        )

        self._title = title
        self._message = message
        self._on_confirm = on_confirm

        self._confirm_button = pygame.Rect(
            0,
            0,
            140,
            45,
        )

        self._cancel_button = pygame.Rect(
            0,
            0,
            140,
            45,
        )

        self._confirm_button.bottomright = (
            self._panel.right - self._padding,
            self._panel.bottom - self._padding,
        )

        self._cancel_button.bottomleft = (
            self._panel.left + self._padding,
            self._panel.bottom - self._padding,
        )

    # ==================================================
    # Draw
    # ==================================================

    def _draw_content(
        self,
        screen: pygame.Surface,
    ):

        title = Fonts.title.render(
            self._title,
            True,
            styles.DIALOGUE_TITLE,
        )

        title_rect = title.get_rect(
            midtop=(
                self._panel.centerx,
                self._panel.top + self._padding,
            )
        )

        screen.blit(
            title,
            title_rect,
        )

        message = Fonts.default.render(
            self._message,
            True,
            styles.DIALOGUE_TEXT,
        )

        message_rect = message.get_rect(
            center=(
                self._panel.centerx,
                self._panel.centery,
            )
        )

        screen.blit(
            message,
            message_rect,
        )

        self._draw_button(
            screen,
            self._cancel_button,
            "Cancelar",
            styles.BUTTON_CANCEL,
        )

        self._draw_button(
            screen,
            self._confirm_button,
            "Confirmar",
            styles.BUTTON_CONFIRM,
        )

    # --------------------------------------------------

    def _draw_button(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        text: str,
        background,
    ):

        pygame.draw.rect(
            screen,
            background,
            rect,
            border_radius=styles.BUTTON_RADIUS,
        )

        label = Fonts.default.render(
            text,
            True,
            styles.BUTTON_TEXT,
        )

        label_rect = label.get_rect(
            center=rect.center,
        )

        screen.blit(
            label,
            label_rect,
        )

    # ==================================================
    # Events
    # ==================================================

    def handle_event(
        self,
        event,
    ) -> bool:

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        if self._cancel_button.collidepoint(
            event.pos
        ):

            self.close()

            return True

        if self._confirm_button.collidepoint(
            event.pos
        ):

            if self._on_confirm is not None:
                self._on_confirm()

            self.close()

            return True

        return True