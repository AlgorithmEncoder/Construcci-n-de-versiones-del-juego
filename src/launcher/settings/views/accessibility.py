"""
Accessibility settings view.

Provides accessibility options related to text size,
visual contrast, motion and dialogue presentation.
"""

from __future__ import annotations

import pygame

from launcher import styles

from launcher.settings.views.base_view import BaseView
from launcher.fonts import Fonts

from launcher import styles as launcher_styles
from game import styles as game_styles
from ui.computer import styles as computer_styles


class AccessibilityView(BaseView):
    """
    Settings view for accessibility options.
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

    TEXT_SIZES = (
        0.80,
        0.90,
        1.00,
        1.10,
        1.20,
        1.30,
        1.50,
    )

    DIALOGUE_SPEEDS = (
        20,
        30,
        40,
        50,
        60,
        80,
        100,
    )

    # ==================================================
    # Construction
    # ==================================================

    def __init__(self, settings_manager, laungage_manager):
        
        self._language = laungage_manager
        
        title = self._language.get(
            "launcher",
            "settings",
            "accessibility",
            "title"
        )
        description = self._language.get(
            "launcher",
            "settings",
            "accessibility",
            "description"
        )

        super().__init__(
            settings_manager=settings_manager,
            section="accessibility",
            title=title,
            description=description,
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

        # ==================================================
        # Text size
        # ==================================================

        if self._controls.get(
            "text_size_left",
            pygame.Rect(0, 0, 0, 0)
        ).collidepoint(content_pos):

            self._change_text_size(-1)

            return True

        if self._controls.get(
            "text_size_right",
            pygame.Rect(0, 0, 0, 0)
        ).collidepoint(content_pos):

            self._change_text_size(1)

            return True

        # ==================================================
        # High contrast
        # ==================================================

        if self._rows.get(
            "high_contrast",
            pygame.Rect(0, 0, 0, 0)
        ).collidepoint(content_pos):

            value = not self._get(
                "high_contrast",
                False
            )

            self._set(
                "high_contrast",
                value
            )

            self._apply_high_contrast(
                value
            )

            return True

        # ==================================================
        # Reduce motion
        # ==================================================

        if self._rows.get(
            "reduce_motion",
            pygame.Rect(0, 0, 0, 0)
        ).collidepoint(content_pos):

            self._set(
                "reduce_motion",
                not self._get(
                    "reduce_motion",
                    False
                )
            )

            return True

        # ==================================================
        # Dialogue typing
        # ==================================================

        if self._rows.get(
            "dialogue_typing",
            pygame.Rect(0, 0, 0, 0)
        ).collidepoint(content_pos):

            self._set(
                "dialogue_typing",
                not self._get(
                    "dialogue_typing",
                    True
                )
            )

            return True

        # ==================================================
        # Dialogue typing speed
        # ==================================================

        if self._controls.get(
            "dialogue_typing_speed_left",
            pygame.Rect(0, 0, 0, 0)
        ).collidepoint(content_pos):

            self._change_dialogue_speed(-1)

            return True

        if self._controls.get(
            "dialogue_typing_speed_right",
            pygame.Rect(0, 0, 0, 0)
        ).collidepoint(content_pos):

            self._change_dialogue_speed(1)

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
        Draws the accessibility settings content.
        """

        self._rows.clear()
        self._controls.clear()

        x = rect.x + 10
        width = rect.width - 20

        y = rect.y + 10

        # ==================================================
        # Text size
        # ==================================================

        self._draw_text_size_row(
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
        # High contrast
        # ==================================================

        constrast_title = self._language.get(
            "launcher",
            "settings",
            "accessibility",
            "high_contrast",
            "title"
        )
        contrast_description = self._language.get(
            "launcher",
            "settings",
            "accessibility",
            "high_contrast",
            "description"
        )
        self._draw_toggle_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                self.ROW_HEIGHT
            ),
            "high_contrast",
            constrast_title,
            contrast_description
        )

        y += self.ROW_HEIGHT + self.ROW_GAP

        # ==================================================
        # Reduce motion
        # ==================================================

        motion_title = self._language.get(
            "launcher",
            "settings",
            "accessibility",
            "reduce_motion",
            "title"
        )
        motion_description = self._language.get(
            "launcher",
            "settings",
            "accessibility",
            "reduce_motion",
            "description"
        )
        self._draw_toggle_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                self.ROW_HEIGHT
            ),
            "reduce_motion",
            motion_title,
            motion_description
        )

        y += self.ROW_HEIGHT + self.ROW_GAP

        # ==================================================
        # Dialogue typing
        # ==================================================

        dialogue_typing_enabled = bool(
            self._get(
                "dialogue_typing",
                True
            )
        )

        typing_title = self._language.get(
            "launcher",
            "settings",
            "accessibility",
            "dialogue_typing",
            "title"
        )
        typing_description = self._language.get(
            "launcher",
            "settings",
            "accessibility",
            "dialogue_typing",
            "description"
        )
        self._draw_toggle_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                self.ROW_HEIGHT
            ),
            "dialogue_typing",
            typing_title,
            typing_description
        )

        y += self.ROW_HEIGHT + self.ROW_GAP

        # ==================================================
        # Dialogue typing speed
        # ==================================================

        self._draw_dialogue_speed_row(
            screen,
            pygame.Rect(
                x,
                y,
                width,
                self.ROW_HEIGHT
            ),
            enabled=dialogue_typing_enabled
        )

    # ==================================================
    # Text size
    # ==================================================

    def _draw_text_size_row(
        self,
        screen,
        rect: pygame.Rect
    ):
        """
        Draws the text size selector.
        """

        self._draw_panel(
            screen,
            rect
        )

        text_x = rect.x + 18

        title_text = self._language.get(
            "launcher",
            "settings",
            "accessibility",
            "text_size",
            "title"
        )
        title = Fonts.default.render(
            title_text,
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

        description_text = self._language.get(
            "launcher",
            "settings",
            "accessibility",
            "text_size",
            "description"
        )
        description = Fonts.small.render(
            description_text,
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

        current = self._get_text_size()

        control_y = (
            rect.y +
            (
                rect.height -
                self.BUTTON_HEIGHT
            ) // 2
        )

        right = rect.right - 18

        # --------------------------------------------------
        # Right button
        # --------------------------------------------------

        arrow_right = pygame.Rect(
            right - 34,
            control_y,
            34,
            self.BUTTON_HEIGHT
        )

        self._controls[
            "text_size_right"
        ] = arrow_right

        self._draw_button(
            screen,
            arrow_right,
            ">"
        )

        # --------------------------------------------------
        # Value
        # --------------------------------------------------

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
            self._text_size_label(current)
        )

        # --------------------------------------------------
        # Left button
        # --------------------------------------------------

        right = value_rect.left - 8

        arrow_left = pygame.Rect(
            right - 34,
            control_y,
            34,
            self.BUTTON_HEIGHT
        )

        self._controls[
            "text_size_left"
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
        """
        Draws a standard accessibility toggle row.
        """

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
    # Dialogue speed
    # ==================================================

    def _draw_dialogue_speed_row(
        self,
        screen,
        rect: pygame.Rect,
        enabled: bool = True
    ):
        """
        Draws the dialogue typing speed selector.

        The selector remains visible when dialogue typing
        is disabled, but is visually disabled.
        """

        self._draw_panel(
            screen,
            rect
        )

        text_x = rect.x + 18

        text_color = (
            styles.TEXT
            if enabled
            else styles.TEXT_SECONDARY
        )

        description_color = styles.TEXT_SECONDARY

        title_text = self._language.get(
            "launcher",
            "settings",
            "accessibility",
            "dialogue_typing_speed",
            "title"
        )
        title = Fonts.default.render(
            title_text,
            True,
            text_color
        )

        screen.blit(
            title,
            (
                text_x,
                rect.y + 15
            )
        )

        description_text = self._language.get(
            "launcher",
            "settings",
            "accessibility",
            "dialogue_typing_speed",
            "description"
        )
        description = Fonts.small.render(
            description_text,
            True,
            description_color
        )

        screen.blit(
            description,
            (
                text_x,
                rect.y + 43
            )
        )

        current = self._get_dialogue_speed()

        control_y = (
            rect.y +
            (
                rect.height -
                self.BUTTON_HEIGHT
            ) // 2
        )

        right = rect.right - 18

        # --------------------------------------------------
        # Right button
        # --------------------------------------------------

        arrow_right = pygame.Rect(
            right - 34,
            control_y,
            34,
            self.BUTTON_HEIGHT
        )

        if enabled:

            self._controls[
                "dialogue_typing_speed_right"
            ] = arrow_right

        self._draw_button(
            screen,
            arrow_right,
            ">",
            enabled=enabled
        )

        # --------------------------------------------------
        # Value
        # --------------------------------------------------

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
            self._dialogue_speed_label(current),
            enabled=enabled
        )

        # --------------------------------------------------
        # Left button
        # --------------------------------------------------

        right = value_rect.left - 8

        arrow_left = pygame.Rect(
            right - 34,
            control_y,
            34,
            self.BUTTON_HEIGHT
        )

        if enabled:

            self._controls[
                "dialogue_typing_speed_left"
            ] = arrow_left

        self._draw_button(
            screen,
            arrow_left,
            "<",
            enabled=enabled
        )

    # ==================================================
    # Controls
    # ==================================================

    def _draw_button(
        self,
        screen,
        rect: pygame.Rect,
        text: str,
        enabled: bool = True
    ):
        """
        Draws a standard selector button.
        """

        if enabled:

            background = styles.PANEL
            border = styles.BORDER
            text_color = styles.TEXT

        else:

            background = styles.SIDEBAR
            border = styles.BORDER
            text_color = styles.TEXT_SECONDARY

        pygame.draw.rect(
            screen,
            background,
            rect,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            border,
            rect,
            1,
            border_radius=6
        )

        surface = Fonts.small.render(
            text,
            True,
            text_color
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
        text: str,
        enabled: bool = True
    ):
        """
        Draws a selector value box.
        """

        background = (
            styles.SIDEBAR
            if enabled
            else styles.BACKGROUND
        )

        text_color = (
            styles.TEXT
            if enabled
            else styles.TEXT_SECONDARY
        )

        pygame.draw.rect(
            screen,
            background,
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
            text_color
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
        """
        Draws a standard toggle.
        """

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
    # Text size helpers
    # ==================================================

    def _get_text_size(self):
        """
        Returns the current text size.
        """

        value = self._get(
            "text_size",
            1.0
        )

        try:

            value = float(value)

        except (
            TypeError,
            ValueError
        ):

            return 1.0

        return value

    # --------------------------------------------------

    def _change_text_size(
        self,
        direction: int
    ):
        """
        Changes the text size to the next available value.
        """

        current = self._get_text_size()

        try:

            index = self.TEXT_SIZES.index(
                current
            )

        except ValueError:

            index = 2

        index = (
            index +
            direction
        ) % len(self.TEXT_SIZES)

        self._set(
            "text_size",
            self.TEXT_SIZES[index]
        )

    # --------------------------------------------------

    @staticmethod
    def _text_size_label(
        value: float
    ):
        """
        Returns the presentation label for a text size.
        """

        return f"{int(value * 100)}%"

    # ==================================================
    # Dialogue speed helpers
    # ==================================================

    def _get_dialogue_speed(self):
        """
        Returns the current dialogue typing speed.
        """

        value = self._get(
            "dialogue_typing_speed",
            40
        )

        try:

            return int(value)

        except (
            TypeError,
            ValueError
        ):

            return 40

    # --------------------------------------------------

    def _change_dialogue_speed(
        self,
        direction: int
    ):
        """
        Changes the dialogue typing speed to the next
        available value.
        """

        current = self._get_dialogue_speed()

        try:

            index = self.DIALOGUE_SPEEDS.index(
                current
            )

        except ValueError:

            index = 2

        index = (
            index +
            direction
        ) % len(self.DIALOGUE_SPEEDS)

        self._set(
            "dialogue_typing_speed",
            self.DIALOGUE_SPEEDS[index]
        )

    # --------------------------------------------------

    def _dialogue_speed_label(self, value: int):
        """
        Returns the presentation label for dialogue speed.
        """

        key = {
            20: "very_slow",
            30: "slow",
            40: "normal",
            50: "fast",
            60: "very_fast",
            80: "fast_plus",
            100: "very_fast_plus",
        }.get(value)

        if key is None:
            return f"{value} caracteres/s"

        return self._language.get(
            "launcher",
            "settings",
            "accessibility",
            "dialogue_typing_speed",
            "values",
            key
        )
    
    def _apply_high_contrast(self, enabled: bool):
        """
        Applies or removes the high contrast visual theme.

        When enabled, all interfaces use the high contrast theme
        without modifying the user's saved theme selections.

        When disabled, the previously selected themes are restored
        from the display settings.
        """

        if enabled:

            launcher_styles.set_theme(
                "high_contrast"
            )

            game_styles.set_theme(
                "high_contrast"
            )

            computer_styles.set_theme(
                "high_contrast"
            )

            return

        display = self._settings_manager.get(
            "display"
        )

        launcher_theme = display.get(
            "launcher_theme",
            "default"
        )

        game_theme = display.get(
            "game_theme",
            "default"
        )

        computer_theme = display.get(
            "computer_theme",
            "default"
        )

        launcher_styles.set_theme(
            launcher_theme
        )

        game_styles.set_theme(
            game_theme
        )

        computer_styles.set_theme(
            computer_theme
        )

    # ==================================================
    # Content height
    # ==================================================

    def _get_content_height(
        self,
        rect
    ):
        """
        Returns the total height required by the section.
        """

        return (
            5 * self.ROW_HEIGHT
            + 4 * self.ROW_GAP
            + 20
        )