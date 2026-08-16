"""
Language settings view.

Provides independent language selection for the launcher,
game interface and the different localized content blocks.

This view only modifies the local language configuration.
Persistence is handled by BaseView.save().
"""

from __future__ import annotations

import pygame

from launcher import styles
from launcher.fonts import Fonts

from launcher.settings.views.base_view import BaseView


class LanguageView(BaseView):
    """
    Settings view for language configuration.

    Each content block can have its own language. Changes
    remain local until save() is called by the settings
    controller when leaving the section.
    """

    # ==================================================
    # Layout
    # ==================================================

    ROW_HEIGHT = 76
    ROW_GAP = 12

    SELECTOR_WIDTH = 180
    SELECTOR_HEIGHT = 40

    # ==================================================
    # Available languages
    # ==================================================

    LANGUAGES = (
        ("es", "Español"),
        ("en", "English"),
        ("va", "Valencià"),
    )

    # ==================================================
    # Language groups
    # ==================================================

    LANGUAGE_OPTIONS = (
        "launcher_interface",
        "game_interface",
        "documents",
        "story",
        "dialogues",
        "computer_messages",
        "computer_files",
    )

    # ==================================================
    # Construction
    # ==================================================

    def __init__(self, settings_manager, launguage_manager):
        
        self._language = launguage_manager
        
        title = self._language.get(
            "launcher",
            "settings",
            "language",
            "title"
        )
        description = self._language.get(
            "launcher",
            "settings",
            "language",
            "description"
        )

        super().__init__(
            settings_manager=settings_manager,
            section="language",
            title=title,
            description=description,
        )

        self._section = "language"

        self._rows: dict[str, pygame.Rect] = {}

        self._selector_rects: dict[
            str,
            pygame.Rect
        ] = {}

    # ==================================================
    # Public API
    # ==================================================

    def handle_event(
        self,
        event
    ):

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
            (
                mouse_x,
                mouse_y
            )
        ):
            return False

        content_pos = (
            mouse_x - self._content_rect.x,
            mouse_y - self._content_rect.y
            + self._scroll_y
        )

        # --------------------------------------------------
        # Language selectors
        # --------------------------------------------------

        for key, selector_rect in (
            self._selector_rects.items()
        ):

            if not selector_rect.collidepoint(
                content_pos
            ):
                continue

            self._cycle_language(
                key
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
        Draws the language settings content.
        """

        x = rect.x + 10
        width = rect.width - 20

        self._rows.clear()
        self._selector_rects.clear()

        y = rect.y + 10

        # ==================================================
        # Language settings
        # ==================================================

        for key in self.LANGUAGE_OPTIONS:

            row = pygame.Rect(
                x,
                y,
                width,
                self.ROW_HEIGHT
            )
            
            title = self._language.get(
                "launcher",
                "settings",
                "language",
                key,
                "title"
            )
            description = self._language.get(
                "launcher",
                "settings",
                "language",
                key,
                "description"
            )

            self._draw_language_row(
                screen,
                row,
                key,
                title,
                description
            )

            y += (
                self.ROW_HEIGHT
                + self.ROW_GAP
            )

    # ==================================================
    # Language row
    # ==================================================

    def _draw_language_row(
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
        # Selector
        # --------------------------------------------------

        selector = pygame.Rect(
            rect.right
            - self.SELECTOR_WIDTH
            - 18,
            rect.y
            + (
                rect.height
                - self.SELECTOR_HEIGHT
            ) // 2,
            self.SELECTOR_WIDTH,
            self.SELECTOR_HEIGHT
        )

        self._selector_rects[key] = selector

        self._draw_selector(
            screen,
            selector,
            self._get(
                key,
                "es"
            )
        )

    # ==================================================
    # Selector
    # ==================================================

    def _draw_selector(
        self,
        screen,
        rect: pygame.Rect,
        language_code: str
    ):

        language_name = self._get_language_name(
            language_code
        )

        # --------------------------------------------------
        # Background
        # --------------------------------------------------

        pygame.draw.rect(
            screen,
            styles.WORKSPACE,
            rect,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            styles.BORDER,
            rect,
            width=1,
            border_radius=6
        )

        # --------------------------------------------------
        # Language
        # --------------------------------------------------

        language_surface = Fonts.default.render(
            language_name,
            True,
            styles.TEXT
        )

        language_rect = language_surface.get_rect(
            midleft=(
                rect.x + 14,
                rect.centery
            )
        )

        screen.blit(
            language_surface,
            language_rect
        )

        # --------------------------------------------------
        # Arrow
        # --------------------------------------------------

        arrow_surface = Fonts.small.render(
            "›",
            True,
            styles.TEXT_SECONDARY
        )

        arrow_rect = arrow_surface.get_rect(
            midright=(
                rect.right - 12,
                rect.centery
            )
        )

        screen.blit(
            arrow_surface,
            arrow_rect
        )

    # ==================================================
    # Language handling
    # ==================================================

    def _cycle_language(
        self,
        key: str
    ):
        """
        Advances the selected language for a setting.

        Languages are cycled in the order defined by
        LANGUAGES.
        """

        current = self._get(
            key,
            "es"
        )

        language_codes = [
            code
            for code, _name
            in self.LANGUAGES
        ]

        try:

            index = language_codes.index(
                current
            )

        except ValueError:

            index = 0

        next_index = (
            index + 1
        ) % len(language_codes)

        self._set(
            key,
            language_codes[next_index]
        )

    # --------------------------------------------------

    @classmethod
    def _get_language_name(
        cls,
        language_code: str
    ) -> str:
        """
        Returns the display name of a language.
        """

        for code, name in cls.LANGUAGES:

            if code == language_code:
                return name

        return language_code

    # ==================================================
    # Content height
    # ==================================================

    def _get_content_height(
        self,
        rect
    ):
        """
        Returns the total height required by the view.
        """

        rows = len(
            self.LANGUAGE_OPTIONS
        )

        return (
            10
            + (
                rows
                * self.ROW_HEIGHT
            )
            + (
                max(
                    0,
                    rows - 1
                )
                * self.ROW_GAP
            )
            + 10
        )