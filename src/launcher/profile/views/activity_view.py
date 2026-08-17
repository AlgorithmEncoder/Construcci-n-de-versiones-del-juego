"""
Activity view.

Displays the persistent activity generated throughout the game.
"""

from __future__ import annotations

from datetime import datetime

import pygame

from launcher import styles
from launcher.fonts import Fonts


class ActivityView:

    """
    Displays the global activity log.
    """

    ENTRY_HEIGHT = 82

    SCROLL_STEP = 3

    # ==================================================
    # Construction
    # ==================================================

    def __init__(
        self,
        logger,
        language_manager
    ):

        self._logger = logger
        self._language = language_manager

        self._scroll = 0
        self._visible_entries = 0

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
        pass

    # --------------------------------------------------

    def draw(
        self,
        screen,
        area
    ):

        self._content_rect = pygame.Rect(
            area.x,
            area.y,
            area.width,
            area.height
        )

        pygame.draw.rect(
            screen,
            styles.BACKGROUND,
            self._content_rect
        )

        self._draw_header(
            screen,
            area
        )

        entries = list(
            reversed(
                self._logger.entries
            )
        )

        if not entries:

            self._draw_empty(
                screen,
                area
            )

            return

        content_top = (
            area.y + 85
        )

        content_rect = pygame.Rect(
            area.x + 12,
            content_top + 8,
            area.width - 24,
            area.bottom
            - content_top
            - 16
        )

        self._visible_entries = max(
            1,
            content_rect.height //
            self.ENTRY_HEIGHT
        )

        max_scroll = max(
            0,
            len(entries)
            - self._visible_entries
        )

        self._scroll = max(
            0,
            min(
                self._scroll,
                max_scroll
            )
        )

        visible = entries[
            self._scroll:
            self._scroll
            + self._visible_entries
            + 1
        ]

        self._draw_entries(
            screen,
            content_rect,
            visible
        )

        self._draw_scroll_indicator(
            screen,
            content_rect,
            len(entries),
            max_scroll
        )

    # --------------------------------------------------

    def handle_event(
        self,
        event
    ):

        if event.type == pygame.MOUSEWHEEL:

            if self._content_rect.collidepoint(
                pygame.mouse.get_pos()
            ):

                self._scroll -= (
                    event.y *
                    self.SCROLL_STEP
                )

                self._clamp_scroll()

                return True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:

                self._scroll -= 1

                self._clamp_scroll()

                return True

            if event.key == pygame.K_DOWN:

                self._scroll += 1

                self._clamp_scroll()

                return True

            if event.key == pygame.K_PAGEUP:

                self._scroll -= (
                    self._visible_entries
                )

                self._clamp_scroll()

                return True

            if event.key == pygame.K_PAGEDOWN:

                self._scroll += (
                    self._visible_entries
                )

                self._clamp_scroll()

                return True

            if event.key == pygame.K_HOME:

                self._scroll = 0

                return True

            if event.key == pygame.K_END:

                entries = self._logger.entries

                self._scroll = max(
                    0,
                    len(entries)
                    - self._visible_entries
                )

                return True

        return False

    # ==================================================
    # Header
    # ==================================================

    def _draw_header(
        self,
        screen,
        area
    ):

        title = Fonts.title.render(
            self._text(
                "activity.title",
                fallback="Actividad"
            ),
            True,
            styles.TEXT
        )

        screen.blit(
            title,
            (
                area.x + 10,
                area.y + 10
            )
        )

        subtitle = Fonts.small.render(
            self._text(
                "activity.subtitle",
                fallback="Registro de acontecimientos"
            ),
            True,
            styles.TEXT_SECONDARY
        )

        screen.blit(
            subtitle,
            (
                area.x + 10,
                area.y + 50
            )
        )

    # ==================================================
    # Empty state
    # ==================================================

    def _draw_empty(
        self,
        screen,
        area
    ):

        text = Fonts.default.render(
            self._text(
                "activity.empty",
                fallback=(
                    "Todavía no hay actividad registrada."
                )
            ),
            True,
            styles.TEXT_SECONDARY
        )

        rect = text.get_rect(
            center=area.center
        )

        screen.blit(
            text,
            rect
        )

    # ==================================================
    # Entries
    # ==================================================

    def _draw_entries(
        self,
        screen,
        area,
        entries
    ):

        old_clip = screen.get_clip()

        screen.set_clip(
            area
        )

        y = area.y

        for entry in entries:

            self._draw_entry(
                screen,
                entry,
                pygame.Rect(
                    area.x,
                    y,
                    area.width,
                    self.ENTRY_HEIGHT - 8
                )
            )

            y += self.ENTRY_HEIGHT

        screen.set_clip(
            old_clip
        )

    # --------------------------------------------------

    def _draw_entry(
        self,
        screen,
        entry,
        rect
    ):

        pygame.draw.rect(
            screen,
            styles.PANEL,
            rect,
            border_radius=8
        )

        timestamp = self._format_timestamp(
            entry.get(
                "timestamp",
                ""
            )
        )

        category = self._format_category(
            entry.get(
                "category",
                "general"
            )
        )

        message = self._get_entry_message(
            entry
        )

        # ==================================================
        # Date
        # ==================================================

        date_surface = Fonts.small.render(
            timestamp,
            True,
            styles.TEXT_SECONDARY
        )

        screen.blit(
            date_surface,
            (
                rect.x + 14,
                rect.y + 10
            )
        )

        # ==================================================
        # Category
        # ==================================================

        category_surface = Fonts.small.render(
            category.upper(),
            True,
            styles.TEXT_LIGHT
        )

        category_rect = category_surface.get_rect()

        category_rect.topright = (
            rect.right - 14,
            rect.y + 10
        )

        category_background = category_rect.inflate(
            16,
            6
        )

        pygame.draw.rect(
            screen,
            styles.PRIMARY,
            category_background,
            border_radius=5
        )

        screen.blit(
            category_surface,
            category_rect
        )

        # ==================================================
        # Message
        # ==================================================

        message_surface = Fonts.default.render(
            message,
            True,
            styles.TEXT
        )

        message_rect = message_surface.get_rect(
            topleft=(
                rect.x + 14,
                rect.y + 40
            )
        )

        max_width = (
            rect.width - 28
        )

        if message_surface.get_width() > max_width:

            message_surface = self._truncate_text(
                message,
                max_width
            )

        screen.blit(
            message_surface,
            message_rect
        )

    # ==================================================
    # Activity text
    # ==================================================

    def _get_entry_message(
        self,
        entry
    ) -> str:
        """
        Resolves an activity entry into presentation text.

        New entries use message_key + parameters.

        Legacy entries containing message are still supported.
        """

        message_key = entry.get(
            "message_key"
        )

        if message_key:

            parameters = entry.get(
                "parameters",
                {}
            )

            return self._text(
                message_key,
                fallback=message_key,
                **parameters
            )

        # --------------------------------------------------
        # Legacy activity
        # --------------------------------------------------

        return str(
            entry.get(
                "message",
                ""
            )
        )

    # ==================================================
    # Scroll
    # ==================================================

    def _draw_scroll_indicator(
        self,
        screen,
        area,
        total_entries,
        max_scroll
    ):

        if max_scroll <= 0:
            return

        track = pygame.Rect(
            area.right - 5,
            area.y,
            4,
            area.height
        )

        pygame.draw.rect(
            screen,
            styles.SIDEBAR,
            track,
            border_radius=2
        )

        visible_ratio = (
            self._visible_entries /
            total_entries
        )

        thumb_height = max(
            30,
            int(
                track.height *
                visible_ratio
            )
        )

        scroll_ratio = (
            self._scroll /
            max_scroll
        )

        thumb_y = (
            track.y +
            int(
                (
                    track.height -
                    thumb_height
                )
                * scroll_ratio
            )
        )

        thumb = pygame.Rect(
            track.x,
            thumb_y,
            track.width,
            thumb_height
        )

        pygame.draw.rect(
            screen,
            styles.PRIMARY,
            thumb,
            border_radius=2
        )

    # ==================================================
    # Formatting
    # ==================================================

    def _format_category(
        self,
        category
    ):

        category = str(
            category or "general"
        )

        return self._text(
            f"activity.categories.{category}",
            fallback=category.replace(
                "_",
                " "
            ).title()
        )

    # --------------------------------------------------

    def _format_timestamp(
        self,
        timestamp
    ):

        if not timestamp:
            return ""

        try:

            value = datetime.fromisoformat(
                timestamp
            )

            return value.strftime(
                "%d/%m/%Y · %H:%M"
            )

        except ValueError:

            return timestamp

    # --------------------------------------------------

    def _truncate_text(
        self,
        text,
        max_width
    ):

        suffix = "..."

        if Fonts.default.size(
            text
        )[0] <= max_width:

            return Fonts.default.render(
                text,
                True,
                styles.TEXT
            )

        current = ""

        for character in text:

            candidate = (
                current +
                character +
                suffix
            )

            if Fonts.default.size(
                candidate
            )[0] > max_width:

                break

            current += character

        return Fonts.default.render(
            current + suffix,
            True,
            styles.TEXT
        )

    # ==================================================
    # Language
    # ==================================================

    def _text(
        self,
        key: str,
        fallback: str = "",
        **parameters
    ) -> str:

        if "." in key:
            key_list = key.split(".")
        else:
            key_list = [key]

        # ----------------------------------------------
        # Claves procedentes del registro del juego
        # ----------------------------------------------

        if key_list[0] == "game" and key_list[1] == "register":
            key_list = ["activity"] + key_list[2:]

        # ----------------------------------------------
        # Evitar que se pueda pasar "launcher.activity..."
        # ----------------------------------------------

        if key_list and key_list[0] == "launcher":
            key_list = key_list[1:]
        
        # ----------------------------------------------
        # Todas las claves de ActivityView están
        # dentro de launcher.activity
        # ----------------------------------------------

        value = self._language.get(
            "launcher",
            *key_list,
            default=fallback
        )

        if value is None:
            value = fallback

        try:

            return str(value).format(
                **parameters
            )

        except (
            KeyError,
            IndexError,
            ValueError
        ):

            return str(value)
    
    # ==================================================
    # Helpers
    # ==================================================

    def _clamp_scroll(self):

        total_entries = len(
            self._logger.entries
        )

        max_scroll = max(
            0,
            total_entries
            - self._visible_entries
        )

        self._scroll = max(
            0,
            min(
                self._scroll,
                max_scroll
            )
        )