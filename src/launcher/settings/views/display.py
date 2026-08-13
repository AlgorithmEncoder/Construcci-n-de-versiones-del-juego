"""
Display settings view.

Provides display, window, interface scale and visual theme options.
"""

from __future__ import annotations

import pygame

from launcher import styles

from launcher.settings.views.base_view import BaseView
from launcher.fonts import Fonts


class DisplayView(BaseView):
    """
    Settings view for display and visual configuration.
    """

    # ==================================================
    # Layout
    # ==================================================

    ROW_HEIGHT = 76
    ROW_GAP = 12

    BUTTON_HEIGHT = 38

    TOGGLE_WIDTH = 48
    TOGGLE_HEIGHT = 26

    CONTROL_WIDTH = 210

    # ==================================================
    # Available options
    # ==================================================

    RESOLUTIONS = (
        (1280, 720),
        (1366, 768),
        (1440, 900),
        (1536, 864),
        (1536, 1024),
        (1600, 900),
        (1920, 1080),
        (2560, 1440),
    )

    UI_SCALES = (
        0.80,
        0.90,
        1.00,
        1.10,
        1.20,
        1.30,
        1.50,
    )

    THEMES = (
        "default",
    )

    # ==================================================
    # Construction
    # ==================================================

    def __init__(self, settings_manager):

        super().__init__(
            settings_manager=settings_manager,
            section="display",
            title="Pantalla",
            description=(
                "Configura la resolución, la ventana y el aspecto visual."
            ),
        )

        self._rows: dict[str, pygame.Rect] = {}
        self._controls: dict[str, pygame.Rect] = {}

    # ==================================================
    # Public API
    # ==================================================

    def handle_event(self, event):

        # --------------------------------------------------
        # Common events
        # --------------------------------------------------

        if super().handle_event(event):
            return True

        # --------------------------------------------------
        # Mouse buttons
        # --------------------------------------------------

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        # --------------------------------------------------
        # Screen -> content coordinates
        # --------------------------------------------------

        mouse_x, mouse_y = event.pos

        if not self._content_rect.collidepoint(
            (mouse_x, mouse_y)
        ):
            return False

        content_pos = (
            mouse_x - self._content_rect.x,
            mouse_y - self._content_rect.y
            + self._scroll_y
        )

        # --------------------------------------------------
        # Resolution
        # --------------------------------------------------

        if self._controls.get(
            "resolution_left",
            pygame.Rect(0,0,0,0)
        ).collidepoint(content_pos):

            self._change_resolution(-1)

            return True

        if self._controls.get(
            "resolution_right",
            pygame.Rect(0,0,0,0)
        ).collidepoint(content_pos):

            self._change_resolution(1)

            return True

        # --------------------------------------------------
        # Fullscreen
        # --------------------------------------------------

        if self._rows.get(
            "fullscreen",
            pygame.Rect(0,0,0,0)
        ).collidepoint(content_pos):

            self._set(
                "fullscreen",
                not self._get(
                    "fullscreen",
                    False
                )
            )

            return True

        # --------------------------------------------------
        # VSync
        # --------------------------------------------------

        if self._rows.get(
            "vsync",
            pygame.Rect(0,0,0,0)
        ).collidepoint(content_pos):

            self._set(
                "vsync",
                not self._get(
                    "vsync",
                    True
                )
            )

            return True

        # --------------------------------------------------
        # UI scale
        # --------------------------------------------------

        if self._controls.get(
            "scale_left",
            pygame.Rect(0,0,0,0)
        ).collidepoint(content_pos):

            self._change_scale(-1)

            return True

        if self._controls.get(
            "scale_right",
            pygame.Rect(0,0,0,0)
        ).collidepoint(content_pos):

            self._change_scale(1)

            return True

        # --------------------------------------------------
        # Launcher theme
        # --------------------------------------------------

        if self._controls.get(
            "launcher_theme_left",
            pygame.Rect(0,0,0,0)
        ).collidepoint(content_pos):

            self._change_theme(
                "launcher_theme",
                -1
            )

            return True

        if self._controls.get(
            "launcher_theme_right",
            pygame.Rect(0,0,0,0)
        ).collidepoint(content_pos):

            self._change_theme(
                "launcher_theme",
                1
            )

            return True

        # --------------------------------------------------
        # Game theme
        # --------------------------------------------------

        if self._controls.get(
            "game_theme_left",
            pygame.Rect(0,0,0,0)
        ).collidepoint(content_pos):

            self._change_theme(
                "game_theme",
                -1
            )

            return True

        if self._controls.get(
            "game_theme_right",
            pygame.Rect(0,0,0,0)
        ).collidepoint(content_pos):

            self._change_theme(
                "game_theme",
                1
            )

            return True

        # --------------------------------------------------
        # Computer theme
        # --------------------------------------------------

        if self._controls.get(
            "computer_theme_left",
            pygame.Rect(0,0,0,0)
        ).collidepoint(content_pos):

            self._change_theme(
                "computer_theme",
                -1
            )

            return True

        if self._controls.get(
            "computer_theme_right",
            pygame.Rect(0,0,0,0)
        ).collidepoint(content_pos):

            self._change_theme(
                "computer_theme",
                1
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
        Draws the display settings content.
        """

        self._rows.clear()
        self._controls.clear()

        x = rect.x + 10
        width = rect.width - 20

        y = rect.y + 10

        # ==================================================
        # Resolution
        # ==================================================

        self._draw_resolution_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                self.ROW_HEIGHT
            )
        )

        y += self.ROW_HEIGHT + self.ROW_GAP

        # ==================================================
        # Fullscreen
        # ==================================================

        self._draw_toggle_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                self.ROW_HEIGHT
            ),
            "fullscreen",
            "Pantalla completa",
            (
                "Utiliza toda la pantalla para ejecutar "
                "la aplicación."
            )
        )

        y += self.ROW_HEIGHT + self.ROW_GAP

        # ==================================================
        # VSync
        # ==================================================

        self._draw_toggle_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                self.ROW_HEIGHT
            ),
            "vsync",
            "Sincronización vertical",
            (
                "Sincroniza la actualización de la imagen "
                "con la frecuencia de la pantalla."
            )
        )

        y += self.ROW_HEIGHT + self.ROW_GAP

        # ==================================================
        # UI scale
        # ==================================================

        self._draw_scale_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                self.ROW_HEIGHT
            )
        )

        y += self.ROW_HEIGHT + self.ROW_GAP

        # ==================================================
        # Launcher theme
        # ==================================================

        self._draw_theme_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                self.ROW_HEIGHT
            ),
            "launcher_theme",
            "Tema del lanzador",
            (
                "Define el aspecto visual de los menús "
                "y la interfaz principal."
            )
        )

        y += self.ROW_HEIGHT + self.ROW_GAP

        # ==================================================
        # Game theme
        # ==================================================

        self._draw_theme_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                self.ROW_HEIGHT
            ),
            "game_theme",
            "Tema del juego",
            (
                "Define el aspecto visual de la interfaz "
                "durante las incursiones."
            )
        )

        y += self.ROW_HEIGHT + self.ROW_GAP

        # ==================================================
        # Computer theme
        # ==================================================

        self._draw_theme_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                self.ROW_HEIGHT
            ),
            "computer_theme",
            "Tema de los ordenadores",
            (
                "Define el aspecto visual de las interfaces "
                "de los ordenadores."
            )
        )

    # ==================================================
    # Resolution
    # ==================================================

    def _draw_resolution_row(
        self,
        screen,
        rect: pygame.Rect
    ):

        self._draw_panel(
            screen,
            rect
        )

        text_x = rect.x + 18

        title = Fonts.default.render(
            "Resolución",
            True,
            styles.TEXT
        )

        screen.blit(
            title,
            (
                text_x,
                rect.y + 15
            )
        )

        description = Fonts.small.render(
            "Resolución utilizada por la ventana del juego.",
            True,
            styles.TEXT_SECONDARY
        )

        screen.blit(
            description,
            (
                text_x,
                rect.y + 43
            )
        )

        # --------------------------------------------------
        # Resolution selector
        # --------------------------------------------------

        current = self._get_resolution()

        control_y = (
            rect.y +
            (
                rect.height -
                self.BUTTON_HEIGHT
            ) // 2
        )

        right = rect.right - 18

        arrow_right = pygame.Rect(
            right - 34,
            control_y,
            34,
            self.BUTTON_HEIGHT
        )

        self._controls[
            "resolution_right"
        ] = arrow_right

        self._draw_button(
            screen,
            arrow_right,
            ">"
        )

        right = arrow_right.left - 8

        value_rect = pygame.Rect(
            right - 130,
            control_y,
            130,
            self.BUTTON_HEIGHT
        )

        self._draw_value_box(
            screen,
            value_rect,
            f"{current[0]} × {current[1]}"
        )

        right = value_rect.left - 8

        arrow_left = pygame.Rect(
            right - 34,
            control_y,
            34,
            self.BUTTON_HEIGHT
        )

        self._controls[
            "resolution_left"
        ] = arrow_left

        self._draw_button(
            screen,
            arrow_left,
            "<"
        )

    # ==================================================
    # Toggle row
    # ==================================================

    def _draw_toggle_row(
        self,
        screen,
        rect: pygame.Rect,
        key: str,
        title: str,
        description: str
    ):

        self._rows[key] = rect

        self._draw_panel(
            screen,
            rect
        )

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
            value
        )

    # ==================================================
    # Scale
    # ==================================================

    def _draw_scale_row(
        self,
        screen,
        rect: pygame.Rect
    ):

        self._draw_panel(
            screen,
            rect
        )

        text_x = rect.x + 18

        title = Fonts.default.render(
            "Escala de interfaz",
            True,
            styles.TEXT
        )

        screen.blit(
            title,
            (
                text_x,
                rect.y + 15
            )
        )

        description = Fonts.small.render(
            "Ajusta el tamaño de los elementos de la interfaz.",
            True,
            styles.TEXT_SECONDARY
        )

        screen.blit(
            description,
            (
                text_x,
                rect.y + 43
            )
        )

        value = float(
            self._get(
                "scale_ui",
                1.0
            )
        )

        value_text = (
            f"{int(value * 100)}%"
        )

        control_y = (
            rect.y +
            (
                rect.height -
                self.BUTTON_HEIGHT
            ) // 2
        )

        right = rect.right - 18

        arrow_right = pygame.Rect(
            right - 34,
            control_y,
            34,
            self.BUTTON_HEIGHT
        )

        self._controls[
            "scale_right"
        ] = arrow_right

        self._draw_button(
            screen,
            arrow_right,
            ">"
        )

        right = arrow_right.left - 8

        value_rect = pygame.Rect(
            right - 100,
            control_y,
            100,
            self.BUTTON_HEIGHT
        )

        self._draw_value_box(
            screen,
            value_rect,
            value_text
        )

        right = value_rect.left - 8

        arrow_left = pygame.Rect(
            right - 34,
            control_y,
            34,
            self.BUTTON_HEIGHT
        )

        self._controls[
            "scale_left"
        ] = arrow_left

        self._draw_button(
            screen,
            arrow_left,
            "<"
        )

    # ==================================================
    # Theme
    # ==================================================

    def _draw_theme_row(
        self,
        screen,
        rect: pygame.Rect,
        key: str,
        title: str,
        description: str
    ):

        self._draw_panel(
            screen,
            rect
        )

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

        value = self._get(
            key,
            "default"
        )

        control_y = (
            rect.y +
            (
                rect.height -
                self.BUTTON_HEIGHT
            ) // 2
        )

        right = rect.right - 18

        arrow_right = pygame.Rect(
            right - 34,
            control_y,
            34,
            self.BUTTON_HEIGHT
        )

        self._controls[
            f"{key}_right"
        ] = arrow_right

        self._draw_button(
            screen,
            arrow_right,
            ">"
        )

        right = arrow_right.left - 8

        value_rect = pygame.Rect(
            right - 130,
            control_y,
            130,
            self.BUTTON_HEIGHT
        )

        self._draw_value_box(
            screen,
            value_rect,
            self._theme_label(value)
        )

        right = value_rect.left - 8

        arrow_left = pygame.Rect(
            right - 34,
            control_y,
            34,
            self.BUTTON_HEIGHT
        )

        self._controls[
            f"{key}_left"
        ] = arrow_left

        self._draw_button(
            screen,
            arrow_left,
            "<"
        )

    # ==================================================
    # Controls
    # ==================================================

    def _draw_button(
        self,
        screen,
        rect: pygame.Rect,
        text: str
    ):

        pygame.draw.rect(
            screen,
            styles.PANEL,
            rect,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            styles.BORDER,
            rect,
            1,
            border_radius=6
        )

        surface = Fonts.small.render(
            text,
            True,
            styles.TEXT
        )

        text_rect = surface.get_rect(
            center=rect.center
        )

        screen.blit(
            surface,
            text_rect
        )

    # --------------------------------------------------

    def _draw_value_box(
        self,
        screen,
        rect: pygame.Rect,
        text: str
    ):

        pygame.draw.rect(
            screen,
            styles.SIDEBAR,
            rect,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            styles.BORDER,
            rect,
            1,
            border_radius=6
        )

        surface = Fonts.small.render(
            text,
            True,
            styles.TEXT
        )

        text_rect = surface.get_rect(
            center=rect.center
        )

        screen.blit(
            surface,
            text_rect
        )

    # --------------------------------------------------

    def _draw_toggle(
        self,
        screen,
        rect: pygame.Rect,
        value: bool
    ):

        background = (
            styles.ACCENT
            if value
            else styles.BORDER
        )

        pygame.draw.rect(
            screen,
            background,
            rect,
            border_radius=rect.height // 2
        )

        diameter = rect.height - 6

        knob = pygame.Rect(
            0,
            0,
            diameter,
            diameter
        )

        if value:

            knob.center = (
                rect.right -
                rect.height // 2,
                rect.centery
            )

        else:

            knob.center = (
                rect.left +
                rect.height // 2,
                rect.centery
            )

        pygame.draw.ellipse(
            screen,
            styles.PANEL,
            knob
        )

    # ==================================================
    # Resolution helpers
    # ==================================================

    def _get_resolution(self):

        value = self._get(
            "resolution",
            [1536, 1024]
        )

        try:

            return (
                int(value[0]),
                int(value[1])
            )

        except (
            TypeError,
            ValueError,
            IndexError
        ):

            return (
                1536,
                1024
            )

    # --------------------------------------------------

    def _change_resolution(
        self,
        direction: int
    ):

        current = self._get_resolution()

        try:

            index = self.RESOLUTIONS.index(
                current
            )

        except ValueError:

            index = 0

        index = (
            index +
            direction
        ) % len(self.RESOLUTIONS)

        resolution = self.RESOLUTIONS[index]

        self._set(
            "resolution",
            [
                resolution[0],
                resolution[1]
            ]
        )

    # ==================================================
    # Scale helpers
    # ==================================================

    def _change_scale(
        self,
        direction: int
    ):

        current = float(
            self._get(
                "scale_ui",
                1.0
            )
        )

        closest = min(
            self.UI_SCALES,
            key=lambda value: abs(
                value - current
            )
        )

        index = self.UI_SCALES.index(
            closest
        )

        index = max(
            0,
            min(
                len(self.UI_SCALES) - 1,
                index + direction
            )
        )

        self._set(
            "scale_ui",
            self.UI_SCALES[index]
        )

    # ==================================================
    # Theme helpers
    # ==================================================

    def _change_theme(
        self,
        key: str,
        direction: int
    ):

        current = self._get(
            key,
            "default"
        )

        try:

            index = self.THEMES.index(
                current
            )

        except ValueError:

            index = 0

        index = (
            index +
            direction
        ) % len(self.THEMES)

        self._set(
            key,
            self.THEMES[index]
        )

    # --------------------------------------------------

    @staticmethod
    def _theme_label(
        theme: str
    ):

        labels = {
            "default": "Predeterminado",
        }

        return labels.get(
            theme,
            theme
        )

    # ==================================================
    # Local settings helpers
    # ==================================================

    def _get(
        self,
        key: str,
        default=None
    ):

        return self._settings.get(
            key,
            default
        )

    # --------------------------------------------------

    def _set(
        self,
        key: str,
        value
    ):

        self._settings[key] = value
    
    def _get_content_height(
        self,
        rect
    ):

        return (
            7 * self.ROW_HEIGHT
            + 6 * self.ROW_GAP
            + 20
        )