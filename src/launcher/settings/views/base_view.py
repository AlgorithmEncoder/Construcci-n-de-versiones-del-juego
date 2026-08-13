"""
Base settings view.

Provides the common structure and rendering helpers used by
individual settings sections.

This class contains no section-specific settings logic.
"""

from __future__ import annotations

import pygame

from launcher import styles
from launcher.fonts import Fonts


class BaseView:
    """
    Base class for launcher settings views.

    Individual settings views inherit from this class and
    implement their own controls and event handling.

    Each view keeps a local copy of its section settings.
    Changes are only transferred to SettingsManager when
    save() is called.
    """

    # ==================================================
    # Layout
    # ==================================================

    TITLE_HEIGHT = 86
    TITLE_FONT_OFFSET = 48

    PANEL_RADIUS = 8

    # ==================================================
    # Construction
    # ==================================================

    def __init__(
        self,
        settings_manager,
        section: str,
        title: str,
        description: str = "",
    ):

        self._settings_manager = settings_manager

        self._section = section
        self._title = title
        self._description = description

        # Local editable copy.
        #
        # SettingsManager is not modified until save()
        # is explicitly called.
        self._settings = dict(
            settings_manager.get(
                section
            )
        )

        self._content_rect = pygame.Rect(
            0,
            0,
            0,
            0
        )

    # ==================================================
    # Public API
    # ==================================================

    def update(
        self,
        dt
    ):
        """
        Updates the view.

        Override when a section requires dynamic behaviour.
        """

    # --------------------------------------------------

    def handle_event(
        self,
        event
    ):
        """
        Handles an input event.

        Individual views should override this method.

        Returns
        -------
        bool
            True if the event was handled.
        """

        return False

    # --------------------------------------------------

    def draw(
        self,
        screen,
        rect=None
    ):
        """
        Draws the complete settings view.

        Parameters
        ----------
        screen:
            Pygame display surface.

        rect:
            Available workspace rectangle.

            If omitted, the complete screen is used.
        """

        if rect is None:

            rect = screen.get_rect()

        self._content_rect = rect

        self._draw_background(
            screen,
            rect
        )

        self._draw_header(
            screen,
            rect
        )

        self._draw_content(
            screen,
            rect
        )

    # --------------------------------------------------

    def save(self):
        """
        Transfers the local configuration to the
        SettingsManager.

        This does not write settings.json to disk.
        """

        self._settings_manager.save_settings(
            self._section,
            self._settings
        )

    # --------------------------------------------------

    def refresh(self):
        """
        Reloads this section from the SettingsManager.

        This discards unsaved local changes.
        """

        self._settings = dict(
            self._settings_manager.get(
                self._section
            )
        )

    # ==================================================
    # Drawing
    # ==================================================

    def _draw_background(
        self,
        screen,
        rect
    ):
        """
        Draws the workspace background.
        """

        pygame.draw.rect(
            screen,
            styles.WORKSPACE,
            rect
        )

    # --------------------------------------------------

    def _draw_header(
        self,
        screen,
        rect
    ):
        """
        Draws the common title and description.
        """

        x = (
            rect.x
            + styles.PADDING
        )

        y = (
            rect.y
            + styles.PADDING
        )

        title = Fonts.title.render(
            self._title,
            True,
            styles.TEXT
        )

        screen.blit(
            title,
            (
                x,
                y
            )
        )

        if self._description:

            description = Fonts.small.render(
                self._description,
                True,
                styles.TEXT_SECONDARY
            )

            screen.blit(
                description,
                (
                    x,
                    y + self.TITLE_FONT_OFFSET
                )
            )

    # --------------------------------------------------

    def _draw_content(
        self,
        screen,
        rect
    ):
        """
        Draws section-specific content.

        Individual views should override this method.
        """

    # ==================================================
    # Layout helpers
    # ==================================================

    def _set_content_rect(
        self,
        screen,
        rect=None,
        top=None
    ):
        """
        Calculates and stores the available content area.

        Returns
        -------
        pygame.Rect
            Available content rectangle.
        """

        if rect is None:

            rect = screen.get_rect()

        if top is None:

            top = (
                rect.y
                + styles.PADDING
                + self.TITLE_HEIGHT
            )

        self._content_rect = pygame.Rect(
            rect.x + styles.PADDING,
            top,
            rect.width
            - (
                styles.PADDING * 2
            ),
            rect.bottom
            - top
            - styles.PADDING
        )

        return self._content_rect

    # --------------------------------------------------

    def _panel_rect(
        self,
        x: int,
        y: int,
        width: int,
        height: int
    ) -> pygame.Rect:
        """
        Creates a standard settings panel rectangle.
        """

        return pygame.Rect(
            x,
            y,
            width,
            height
        )

    # --------------------------------------------------

    def _draw_panel(
        self,
        screen,
        rect: pygame.Rect
    ):
        """
        Draws a standard launcher panel.
        """

        pygame.draw.rect(
            screen,
            styles.PANEL,
            rect,
            border_radius=self.PANEL_RADIUS
        )

        pygame.draw.rect(
            screen,
            styles.BORDER,
            rect,
            width=1,
            border_radius=self.PANEL_RADIUS
        )

    # --------------------------------------------------

    def _draw_section_title(
        self,
        screen,
        title: str,
        x: int,
        y: int
    ):
        """
        Draws a title inside a settings panel.
        """

        surface = Fonts.default.render(
            title,
            True,
            styles.TEXT
        )

        screen.blit(
            surface,
            (
                x,
                y
            )
        )

    # --------------------------------------------------

    def _draw_label(
        self,
        screen,
        text: str,
        x: int,
        y: int
    ):
        """
        Draws a standard settings label.
        """

        surface = Fonts.default.render(
            text,
            True,
            styles.TEXT
        )

        screen.blit(
            surface,
            (
                x,
                y
            )
        )

    # --------------------------------------------------

    def _draw_description(
        self,
        screen,
        text: str,
        x: int,
        y: int
    ):
        """
        Draws secondary explanatory text.
        """

        surface = Fonts.small.render(
            text,
            True,
            styles.TEXT_SECONDARY
        )

        screen.blit(
            surface,
            (
                x,
                y
            )
        )

    # ==================================================
    # Configuration helpers
    # ==================================================

    def _get(
        self,
        key: str,
        default=None
    ):
        """
        Gets a value from the local section configuration.
        """

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
        """
        Updates a value in the local section configuration.

        SettingsManager is not modified until save()
        is called.
        """

        self._settings[key] = value

    # ==================================================
    # Properties
    # ==================================================

    @property
    def settings(self) -> dict:
        """
        Returns the local configuration of this section.
        """

        return self._settings

    # --------------------------------------------------

    @property
    def section(self) -> str:
        """
        Returns the settings section identifier.
        """

        return self._section

    # --------------------------------------------------

    @property
    def content_rect(self) -> pygame.Rect:
        """
        Returns the currently calculated content rectangle.
        """

        return self._content_rect