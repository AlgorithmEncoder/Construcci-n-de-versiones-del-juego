"""
General settings view.

Provides general application behaviour options.
"""

from __future__ import annotations

import pygame

from launcher import styles

from launcher.settings.views.base_view import BaseView
from launcher.fonts import Fonts


class GeneralView(BaseView):
    """
    Settings view for general application behaviour.
    """

    # ==================================================
    # Layout
    # ==================================================

    ROW_HEIGHT = 76
    ROW_GAP = 12

    TOGGLE_WIDTH = 48
    TOGGLE_HEIGHT = 26

    # ==================================================
    # Construction
    # ==================================================

    def __init__(self, settings_manager):

        super().__init__(
            settings_manager=settings_manager,
            section="general",
            title="General",
            description=(
                "Configura el comportamiento general de la aplicación."
            ),
        )

        self._section = "general"
        self._rows: dict[str, pygame.Rect] = {}

    # ==================================================
    # Public API
    # ==================================================

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        for key, rect in self._rows.items():

            if not rect.collidepoint(event.pos):
                continue

            # ------------------------------------------
            # Disabled settings
            # ------------------------------------------

            if key in (
                "important_notifications",
                "confirm_important_actions",
                "restore_previous_state",
            ):
                return False

            # ------------------------------------------
            # Active settings
            # ------------------------------------------

            if key == "confirm_exit":

                self._set(
                    key,
                    not self._get(
                        key,
                        False
                    )
                )

                return True

        return False

    # ==================================================
    # Content
    # ==================================================

    def _draw_content(
        self,
        screen,
        rect
    ):
        """
        Draws the general settings content.
        """

        x = rect.x + 10
        width = rect.width - 20

        self._rows.clear()

        y = rect.y + 90

        # ==================================================
        # Settings
        # ==================================================

        self._draw_setting_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                72
            ),
            "confirm_exit",
            "Confirmar salida",
            "Muestra una confirmación antes de abandonar una incursión.",
        )

        y += 82

        self._draw_setting_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                72
            ),
            "important_notifications",
            "Avisos importantes",
            "Muestra avisos adicionales sobre acciones importantes.",
            enabled=False
        )

        y += 82

        self._draw_setting_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                72
            ),
            "confirm_important_actions",
            "Confirmar acciones importantes",
            "Solicita confirmación antes de determinadas acciones.",
            enabled=False
        )

        y += 82

        self._draw_setting_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                72
            ),
            "restore_previous_state",
            "Restaurar estado anterior",
            "Permite configurar el comportamiento al volver a abrir el juego.",
            enabled=False
        )

    # ==================================================
    # Setting row
    # ==================================================

    def _draw_setting_row(
        self,
        screen,
        rect: pygame.Rect,
        key: str,
        title: str,
        description: str,
        enabled: bool = True
    ):

        self._rows[key] = rect

        self._draw_panel(
            screen,
            rect
        )

        # --------------------------------------------------
        # Text
        # --------------------------------------------------

        text_x = rect.x + 18

        title_surface = Fonts.default.render(
            title,
            True,
            styles.TEXT
        )

        screen.blit(
            title_surface,
            (
                text_x,
                rect.y + 15
            )
        )

        description_surface = Fonts.small.render(
            description,
            True,
            styles.TEXT_SECONDARY
        )

        screen.blit(
            description_surface,
            (
                text_x,
                rect.y + 43
            )
        )

        # --------------------------------------------------
        # Toggle
        # --------------------------------------------------

        value = bool(
            self._get(
                key,
                False
            )
        )

        toggle = pygame.Rect(
            rect.right -
            self.TOGGLE_WIDTH -
            18,
            rect.y +
            (
                rect.height -
                self.TOGGLE_HEIGHT
            ) // 2,
            self.TOGGLE_WIDTH,
            self.TOGGLE_HEIGHT
        )

        self._draw_toggle(
            screen,
            toggle,
            value,
            enabled=enabled
        )

        # --------------------------------------------------
        # Status
        # --------------------------------------------------

        if not enabled:

            status_surface = Fonts.small.render(
                "No implementado",
                True,
                styles.TEXT_SECONDARY
            )

            status_rect = status_surface.get_rect(
                midright=(
                    toggle.left - 15,
                    toggle.centery
                )
            )

            screen.blit(
                status_surface,
                status_rect
            )

    # ==================================================
    # Toggle
    # ==================================================

    def _draw_toggle(
        self,
        screen,
        rect: pygame.Rect,
        value: bool,
        enabled: bool = True
    ):

        # --------------------------------------------------
        # Background
        # --------------------------------------------------

        if not enabled:

            background = styles.BORDER

        elif value:

            background = styles.ACCENT

        else:

            background = styles.BORDER

        pygame.draw.rect(
            screen,
            background,
            rect,
            border_radius=rect.height // 2
        )

        # --------------------------------------------------
        # Knob
        # --------------------------------------------------

        diameter = rect.height - 6

        knob = pygame.Rect(
            0,
            0,
            diameter,
            diameter
        )

        if value and enabled:

            knob.center = (
                rect.right -
                rect.height // 2,
                rect.centery
            )

        else:

            knob.center = (
                rect.x +
                rect.height // 2,
                rect.centery
            )

        pygame.draw.ellipse(
            screen,
            styles.PANEL,
            knob
        )