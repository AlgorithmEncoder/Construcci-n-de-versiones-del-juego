"""
Achievement manager.

Loads, checks and saves achievement progress.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

from constants import DATA_DIR

from launcher.profile.achievements.achievement_checks import (
    all_memories_completed,
    chat_reader_10,
    chat_reader_25,
    chat_reader_50,
    chat_reader_100,
    chat_reader_250,
    computer_user_10,
    computer_user_25,
    computer_user_50,
    computer_user_100,
    computer_user_250,
    detected_1,
    detected_5,
    detected_10,
    detected_25,
    detected_50,
    detected_100,
    document_collector_10,
    document_collector_25,
    document_collector_50,
    document_collector_100,
    document_collector_250,
    email_reader_10,
    email_reader_25,
    email_reader_50,
    email_reader_100,
    email_reader_250,
    explorer_10,
    explorer_25,
    explorer_50,
    explorer_100,
    explorer_250,
    file_reader_10,
    file_reader_25,
    file_reader_50,
    file_reader_100,
    file_reader_250,
    first_chat,
    first_computer,
    first_detection,
    first_discovery,
    first_document,
    first_dialogue,
    first_email,
    first_file,
    first_incursion,
    first_memory_completed,
    incursions_5,
    incursions_10,
    incursions_25,
    incursions_50,
    incursions_100,
    iterations_10,
    iterations_25,
    iterations_50,
    iterations_100,
    iterations_250,
    iterations_500,
    memories_completed_1,
    memories_completed_2,
    memories_completed_5,
    memories_completed_10,
    social_10,
)


# ==================================================
# Memory achievements
# ==================================================

MEMORY_ACHIEVEMENT_CHECKS = {
    # First steps
    "first_incursion": first_incursion,
    "first_discovery": first_discovery,
    "first_document": first_document,
    "first_computer": first_computer,
    "first_email": first_email,
    "first_chat": first_chat,
    "first_file": first_file,
    "first_dialogue": first_dialogue,
    "first_detection": first_detection,
    "first_memory_completed": first_memory_completed,

    # Exploration
    "explorer_10": explorer_10,
    "explorer_25": explorer_25,
    "explorer_50": explorer_50,
    "explorer_100": explorer_100,
    "explorer_250": explorer_250,

    # Documents
    "document_collector_10": document_collector_10,
    "document_collector_25": document_collector_25,
    "document_collector_50": document_collector_50,
    "document_collector_100": document_collector_100,
    "document_collector_250": document_collector_250,

    # Computers
    "computer_user_10": computer_user_10,
    "computer_user_25": computer_user_25,
    "computer_user_50": computer_user_50,
    "computer_user_100": computer_user_100,
    "computer_user_250": computer_user_250,

    # Emails
    "email_reader_10": email_reader_10,
    "email_reader_25": email_reader_25,
    "email_reader_50": email_reader_50,
    "email_reader_100": email_reader_100,
    "email_reader_250": email_reader_250,

    # Chats
    "chat_reader_10": chat_reader_10,
    "chat_reader_25": chat_reader_25,
    "chat_reader_50": chat_reader_50,
    "chat_reader_100": chat_reader_100,
    "chat_reader_250": chat_reader_250,

    # Files
    "file_reader_10": file_reader_10,
    "file_reader_25": file_reader_25,
    "file_reader_50": file_reader_50,
    "file_reader_100": file_reader_100,
    "file_reader_250": file_reader_250,

    # Detection
    "detected_1": detected_1,
    "detected_5": detected_5,
    "detected_10": detected_10,
    "detected_25": detected_25,
    "detected_50": detected_50,
    "detected_100": detected_100,

    # Iterations
    "iterations_10": iterations_10,
    "iterations_25": iterations_25,
    "iterations_50": iterations_50,
    "iterations_100": iterations_100,
    "iterations_250": iterations_250,
    "iterations_500": iterations_500,

    # Incursions
    "incursions_5": incursions_5,
    "incursions_10": incursions_10,
    "incursions_25": incursions_25,
    "incursions_50": incursions_50,
    "incursions_100": incursions_100,

    # Social
    "social_10": social_10,
}


# ==================================================
# Global achievements
# ==================================================

GLOBAL_ACHIEVEMENT_CHECKS = {
    "memories_completed_1": memories_completed_1,
    "memories_completed_2": memories_completed_2,
    "memories_completed_5": memories_completed_5,
    "memories_completed_10": memories_completed_10,
    "all_memories_completed": all_memories_completed,
}


# ==================================================
# Combined registry
# ==================================================

ACHIEVEMENT_CHECKS = {
    **MEMORY_ACHIEVEMENT_CHECKS,
    **GLOBAL_ACHIEVEMENT_CHECKS,
}


# ==================================================
# Prerequisites
# ==================================================

ACHIEVEMENT_PREREQUISITES = {
    "explorer_25": "explorer_10",
    "explorer_50": "explorer_25",
    "explorer_100": "explorer_50",
    "explorer_250": "explorer_100",

    "document_collector_25": "document_collector_10",
    "document_collector_50": "document_collector_25",
    "document_collector_100": "document_collector_50",
    "document_collector_250": "document_collector_100",

    "computer_user_25": "computer_user_10",
    "computer_user_50": "computer_user_25",
    "computer_user_100": "computer_user_50",
    "computer_user_250": "computer_user_100",

    "email_reader_25": "email_reader_10",
    "email_reader_50": "email_reader_25",
    "email_reader_100": "email_reader_50",
    "email_reader_250": "email_reader_100",

    "chat_reader_25": "chat_reader_10",
    "chat_reader_50": "chat_reader_25",
    "chat_reader_100": "chat_reader_50",
    "chat_reader_250": "chat_reader_100",

    "file_reader_25": "file_reader_10",
    "file_reader_50": "file_reader_25",
    "file_reader_100": "file_reader_50",
    "file_reader_250": "file_reader_100",

    "detected_5": "detected_1",
    "detected_10": "detected_5",
    "detected_25": "detected_10",
    "detected_50": "detected_25",
    "detected_100": "detected_50",

    "iterations_25": "iterations_10",
    "iterations_50": "iterations_25",
    "iterations_100": "iterations_50",
    "iterations_250": "iterations_100",
    "iterations_500": "iterations_250",

    "incursions_10": "incursions_5",
    "incursions_25": "incursions_10",
    "incursions_50": "incursions_25",
    "incursions_100": "incursions_50",

    "memories_completed_2": "memories_completed_1",
    "memories_completed_5": "memories_completed_2",
    "memories_completed_10": "memories_completed_5",
}


class AchievementsManager:
    """
    Provides access to persistent achievement progress.
    """

    def __init__(self, stats_manager):
        self._stats = stats_manager

        self._path = (
            DATA_DIR
            / "global"
            / "achievements.json"
        )

        self._achievements = {}

        self.load()

    # ==================================================
    # Loading
    # ==================================================

    def load(self):
        self._achievements = {}

        if self._path.exists():
            try:
                with self._path.open(
                    "r",
                    encoding="utf-8"
                ) as file:
                    data = json.load(file)

                if isinstance(data, dict):
                    self._achievements = data

            except (
                OSError,
                json.JSONDecodeError,
                TypeError
            ):
                self._achievements = {}

        self._ensure_entries()

    # --------------------------------------------------

    def _ensure_entries(self):
        changed = False

        for achievement_id in ACHIEVEMENT_CHECKS:
            state = self._achievements.get(
                achievement_id
            )

            if not isinstance(state, dict):
                self._achievements[
                    achievement_id
                ] = {
                    "unlocked": False,
                    "unlocked_at": None,
                }

                changed = True
                continue

            if "unlocked" not in state:
                state["unlocked"] = False
                changed = True

            if "unlocked_at" not in state:
                state["unlocked_at"] = None
                changed = True

        if changed:
            self.save()

    # ==================================================
    # Checking
    # ==================================================

    def check(self):
        """
        Check achievements that depend on global statistics.

        The checks receive the global StatsManager.
        """

        changed = False

        for achievement_id, check in (
            GLOBAL_ACHIEVEMENT_CHECKS.items()
        ):
            if self.is_unlocked(
                achievement_id
            ):
                continue

            if check(self._stats):
                self._unlock(
                    achievement_id
                )
                changed = True

        if changed:
            self.save()

        return changed

    # --------------------------------------------------

    def check_memory(self, stats):
        """
        Check achievements associated with the
        currently played memory.

        `stats` must be the dictionary containing
        the current memory's statistics.

        Prerequisites do NOT prevent unlocking.
        They only control visibility in the UI.
        """

        changed = False

        for achievement_id, check in (
            MEMORY_ACHIEVEMENT_CHECKS.items()
        ):
            if self.is_unlocked(
                achievement_id
            ):
                continue

            if check(stats):
                self._unlock(
                    achievement_id
                )
                changed = True

        if changed:
            self.save()

        return changed

    # ==================================================
    # Unlocking
    # ==================================================

    def _unlock(self, achievement_id):
        self._achievements[
            achievement_id
        ] = {
            "unlocked": True,
            "unlocked_at": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),
        }

    # ==================================================
    # Persistence
    # ==================================================

    def save(self):
        self._path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with self._path.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self._achievements,
                file,
                indent=4,
                ensure_ascii=False
            )

    # ==================================================
    # Queries
    # ==================================================

    @property
    def achievements(self):
        return self._achievements

    # --------------------------------------------------

    def is_unlocked(self, achievement_id):
        return bool(
            self._achievements.get(
                achievement_id,
                {}
            ).get(
                "unlocked",
                False
            )
        )

    # --------------------------------------------------

    def is_visible(self, achievement_id):
        """
        Determines whether an achievement should show
        its real information in the UI.

        Prerequisites affect presentation only.
        """

        prerequisite = ACHIEVEMENT_PREREQUISITES.get(
            achievement_id
        )

        if prerequisite is None:
            return True

        return self.is_unlocked(
            prerequisite
        )