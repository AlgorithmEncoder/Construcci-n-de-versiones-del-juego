"""
Statistics data access and aggregation.

Loads persistent statistics from the global data directory and
individual memory statistics from their respective memory folders.

This module contains no rendering code.
"""

from __future__ import annotations

import json
from pathlib import Path

from constants import GLOBAL_DIR, MEMORIES_DIR


class StatsManager:
    """
    Provides access to global and per-memory statistics.

    Global statistics are derived from the individual memory
    stats.json files whenever possible, avoiding duplicated
    persistent information.
    """

    def __init__(self):

        self._global_path = (
            GLOBAL_DIR / "stats.json"
        )

        self._memories: dict[str, dict] = {}

        self._load_memories()

    # ==================================================
    # Loading
    # ==================================================

    def _load_memories(self):

        self._memories.clear()

        if not MEMORIES_DIR.exists():
            return

        for memory_dir in sorted(
            MEMORIES_DIR.iterdir()
        ):

            if not memory_dir.is_dir():
                continue

            stats_path = (
                memory_dir / "stats.json"
            )

            if not stats_path.exists():
                continue

            try:

                with stats_path.open(
                    "r",
                    encoding="utf-8"
                ) as file:

                    stats = json.load(file)

            except (
                OSError,
                json.JSONDecodeError
            ):

                continue

            memory_id = memory_dir.name

            self._memories[memory_id] = stats

    # ==================================================
    # Properties
    # ==================================================

    @property
    def memories(self) -> dict[str, dict]:
        """
        Returns all loaded memory statistics.
        """

        return self._memories

    # --------------------------------------------------

    @property
    def unlocked_memories(self) -> list[str]:
        """
        Returns IDs of memories available to the player.
        """

        return [
            memory_id
            for memory_id, stats
            in self._memories.items()
            if not stats.get(
                "state",
                {}
            ).get(
                "locked",
                False
            )
        ]

    # --------------------------------------------------

    @property
    def global_stats(self) -> dict:
        """
        Returns global statistics.

        Values are calculated from individual memory
        statistics instead of being stored redundantly.
        """

        memories = self._memories.values()

        return {
            "incursions": sum(
                self._get_number(
                    stats,
                    "played",
                    "times_incursion"
                )
                for stats in memories
            ),

            "iterations": sum(
                self._get_number(
                    stats,
                    "played",
                    "iterations"
                )
                for stats in memories
            ),

            "total_played": sum(
                self._get_number(
                    stats,
                    "played",
                    "total_played"
                )
                for stats in memories
            ),

            "rooms_visited": sum(
                self._get_number(
                    stats,
                    "exploration",
                    "rooms_visited"
                )
                for stats in memories
            ),

            "documents_opened": sum(
                self._get_number(
                    stats,
                    "exploration",
                    "documents_opened"
                )
                for stats in memories
            ),

            "computers_opened": sum(
                self._get_number(
                    stats,
                    "exploration",
                    "computers_opened"
                )
                for stats in memories
            ),

            "chats_opened": sum(
                self._get_number(
                    stats,
                    "exploration",
                    "chats_opened"
                )
                for stats in memories
            ),

            "emails_read": sum(
                self._get_number(
                    stats,
                    "exploration",
                    "emails_read"
                )
                for stats in memories
            ),

            "files_opened": sum(
                self._get_number(
                    stats,
                    "exploration",
                    "files_opened"
                )
                for stats in memories
            ),

            "detections": sum(
                self._get_number(
                    stats,
                    "detection",
                    "total"
                )
                for stats in memories
            ),

            "completed_memories": sum(
                1
                for stats in memories
                if stats.get(
                    "state",
                    {}
                ).get(
                    "completed",
                    False
                )
            ),

            "unlocked_memories": len(
                self.unlocked_memories
            ),
        }

    # ==================================================
    # Memory access
    # ==================================================

    def get(self, memory_id: str) -> dict | None:
        """
        Returns statistics for a specific memory.
        """

        return self._memories.get(
            memory_id
        )

    # --------------------------------------------------

    def get_title(self, memory_id: str) -> str:
        """
        Reads only the title from story.json.

        No other story information is used by the
        statistics system.
        """

        story_path = (
            MEMORIES_DIR
            / memory_id
            / "story.json"
        )

        if not story_path.exists():
            return memory_id

        try:

            with story_path.open(
                "r",
                encoding="utf-8"
            ) as file:

                story = json.load(file)

            return story.get(
                "title",
                memory_id
            )

        except (
            OSError,
            json.JSONDecodeError
        ):

            return memory_id

    # ==================================================
    # Helpers
    # ==================================================

    @staticmethod
    def _get_number(
        stats: dict,
        section: str,
        key: str
    ) -> int:

        value = stats.get(
            section,
            {}
        ).get(
            key,
            0
        )

        try:
            return int(value)

        except (
            TypeError,
            ValueError
        ):

            return 0
    
    def _unlocked_memories(self):
        return self._stats.unlocked_memories
    
    def _memory_display_name(self, memory):
        if memory is None:
            return "Selecciona una memoria"

        return self._stats.get_title(memory)
    
    def refresh(self):
        self._load_memories()