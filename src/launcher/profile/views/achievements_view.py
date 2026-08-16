"""
Achievements view.

Displays the player's achievement progress.
"""

from __future__ import annotations

from datetime import datetime

import pygame

from ui.fonts import Fonts
from launcher import styles

from launcher.profile.achievements.achievement_builder import (
    AchievementBuilder,
)


class AchievementsView:

    ENTRY_HEIGHT = 92
    HEADER_HEIGHT = 92
    SCROLL_STEP = 3

    # ==================================================
    # Explicit achievement order
    # ==================================================

    ACHIEVEMENT_ORDER = [

        # --------------------------------------------------
        # General / first steps
        # --------------------------------------------------

        "first_incursion",
        "incursions_5",
        "incursions_10",
        "incursions_25",
        "incursions_50",
        "incursions_100",

        # --------------------------------------------------
        # Memory progress
        # --------------------------------------------------

        "first_memory_completed",
        "memories_completed_1",
        "memories_completed_2",
        "memories_completed_5",
        "memories_completed_10",
        "all_memories_completed",

        # --------------------------------------------------
        # Discovery
        # --------------------------------------------------

        "first_discovery",

        # --------------------------------------------------
        # Exploration - rooms
        # --------------------------------------------------

        "explorer_10",
        "explorer_25",
        "explorer_50",
        "explorer_100",
        "explorer_250",

        # --------------------------------------------------
        # Exploration - documents
        # --------------------------------------------------

        "first_document",
        "document_collector_10",
        "document_collector_25",
        "document_collector_50",
        "document_collector_100",
        "document_collector_250",

        # --------------------------------------------------
        # Exploration - computers
        # --------------------------------------------------

        "first_computer",
        "computer_user_10",
        "computer_user_25",
        "computer_user_50",
        "computer_user_100",
        "computer_user_250",

        # --------------------------------------------------
        # Exploration - emails
        # --------------------------------------------------

        "first_email",
        "email_reader_10",
        "email_reader_25",
        "email_reader_50",
        "email_reader_100",
        "email_reader_250",

        # --------------------------------------------------
        # Exploration - chats
        # --------------------------------------------------

        "first_chat",
        "chat_reader_10",
        "chat_reader_25",
        "chat_reader_50",
        "chat_reader_100",
        "chat_reader_250",

        # --------------------------------------------------
        # Exploration - files
        # --------------------------------------------------

        "first_file",
        "file_reader_10",
        "file_reader_25",
        "file_reader_50",
        "file_reader_100",
        "file_reader_250",

        # --------------------------------------------------
        # Exploration - social
        # --------------------------------------------------

        "first_dialogue",
        "social_10",

        # --------------------------------------------------
        # Detection
        # --------------------------------------------------

        "first_detection",
        "detected_1",
        "detected_5",
        "detected_10",
        "detected_25",
        "detected_50",
        "detected_100",

        # --------------------------------------------------
        # Iterations
        # --------------------------------------------------

        "iterations_10",
        "iterations_25",
        "iterations_50",
        "iterations_100",
        "iterations_250",
        "iterations_500",
    ]

    def __init__(
        self,
        achievements,
        language,
        achievement_data=None
    ):

        self._achievements = achievements
        self._language = language

        self._achievement_data = (
            achievement_data
            if isinstance(
                achievement_data,
                dict
            )
            else {}
        )

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

        return None

    # --------------------------------------------------

    def refresh(self):

        self._scroll = 0

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

        entries = self._build_entries()

        self._draw_header(
            screen,
            area,
            entries
        )

        if not entries:

            self._draw_empty(
                screen,
                area
            )

            return

        content_top = (
            area.y +
            self.HEADER_HEIGHT
        )

        content_width = max(
            0,
            area.width - 24
        )

        content_height = max(
            0,
            area.bottom -
            content_top -
            16
        )

        content_rect = pygame.Rect(
            area.x + 12,
            content_top + 8,
            content_width,
            content_height
        )

        self._visible_entries = max(
            1,
            content_rect.height //
            self.ENTRY_HEIGHT
        )

        max_scroll = max(
            0,
            len(entries) -
            self._visible_entries
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
            self._scroll +
            self._visible_entries +
            1
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

    # ==================================================
    # Events
    # ==================================================

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

                self._scroll -= max(
                    1,
                    self._visible_entries
                )

                self._clamp_scroll()

                return True

            if event.key == pygame.K_PAGEDOWN:

                self._scroll += max(
                    1,
                    self._visible_entries
                )

                self._clamp_scroll()

                return True

            if event.key == pygame.K_HOME:

                self._scroll = 0

                return True

            if event.key == pygame.K_END:

                entries = self._build_entries()

                self._scroll = max(
                    0,
                    len(entries) -
                    self._visible_entries
                )

                return True

        return False

    # ==================================================
    # Data
    # ==================================================

    def _build_entries(self):

        entries = AchievementBuilder.build_all(
            self._achievements.achievements,
            self._achievement_data,
            visible_callback=(
                self._achievements.is_visible
            )
        )

        entries_by_id = {
            entry["id"]: entry
            for entry in entries
        }

        ordered_entries = []

        for achievement_id in (
            self.ACHIEVEMENT_ORDER
        ):

            entry = entries_by_id.get(
                achievement_id
            )

            if entry is not None:

                ordered_entries.append(
                    entry
                )

        ordered_ids = set(
            self.ACHIEVEMENT_ORDER
        )

        remaining_entries = [

            entry

            for entry in entries

            if entry["id"] not in ordered_ids
        ]

        ordered_entries.extend(
            remaining_entries
        )

        return ordered_entries

    # ==================================================
    # Header
    # ==================================================

    def _draw_header(
        self,
        screen,
        area,
        entries
    ):

        title = Fonts.title.render(
            self._language.get(
                "launcher",
                "achievements",
                "title"
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

        unlocked = sum(
            1
            for entry in entries
            if entry["unlocked"]
        )

        total = len(entries)

        subtitle = Fonts.small.render(
            self._language.get(
                "launcher",
                "achievements",
                "summary"
            ).format(
                unlocked=unlocked,
                total=total
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
            self._language.get(
                "launcher",
                "achievements",
                "empty"
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

        try:

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

        finally:

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

        title = entry["title"]
        description = entry["description"]

        if entry["hidden"]:

            title = "???"
            description = self._language.get(
                "launcher",
                "achievements",
                "hidden"
            )

        title_surface = Fonts.default.render(
            title,
            True,
            styles.TEXT
        )

        screen.blit(
            title_surface,
            (
                rect.x + 14,
                rect.y + 12
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
                rect.x + 14,
                rect.y + 44
            )
        )

        if entry["unlocked"]:

            timestamp = self._format_timestamp(
                entry["unlocked_at"]
            )

            unlocked_text = self._language.get(
                "launcher",
                "achievements",
                "unlocked"
            ).format(
                timestamp=timestamp
            )

            surface = Fonts.small.render(
                unlocked_text,
                True,
                styles.TEXT_SECONDARY
            )

            screen.blit(
                surface,
                (
                    rect.right - surface.get_width() - 14,
                    rect.y + 12
                )
            )

    # ==================================================
    # Scroll
    # ==================================================

    def _clamp_scroll(self):

        entries = self._build_entries()

        max_scroll = max(
            0,
            len(entries) -
            self._visible_entries
        )

        self._scroll = max(
            0,
            min(
                self._scroll,
                max_scroll
            )
        )

    # --------------------------------------------------

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
            max(
                1,
                total_entries
            )
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
                ) *
                scroll_ratio
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

        except (
            TypeError,
            ValueError
        ):

            return str(timestamp)

        return value.strftime(
            "%d/%m/%Y %H:%M"
        )