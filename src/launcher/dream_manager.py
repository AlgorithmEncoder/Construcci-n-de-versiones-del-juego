"""
dream_manager.py

Loads every available dream (memory) for the launcher.
"""

from __future__ import annotations

import json

from pathlib import Path

from constants import MEMORIES_DIR


class DreamManager:

    def __init__(self):

        self._dreams = []

    # ==================================================
    # Public API
    # ==================================================

    def load(self):

        self._dreams.clear()

        if not MEMORIES_DIR.exists():
            return

        for memory_dir in sorted(MEMORIES_DIR.iterdir()):

            if not memory_dir.is_dir():
                continue

            story_path = memory_dir / "story.json"

            if not story_path.exists():
                continue

            with open(
                story_path,
                encoding="utf-8"
            ) as file:

                story = json.load(file)

            self._dreams.append({

                "id": memory_dir.name,

                "title": story.get(
                    "title",
                    memory_dir.name
                ),

                "description": story.get(
                    "description",
                    ""
                ),

                "objective": story.get(
                    "objective",
                    ""
                ),

                "duration": story.get(
                    "time_limit",
                    0
                ),

                # De momento
                "locked": False,

                "progress": 0,

                "iterations": 0,
            })

    # ==================================================
    # Queries
    # ==================================================

    @property
    def dreams(self):

        return tuple(self._dreams)

    # --------------------------------------------------

    def get(self, dream_id):

        for dream in self._dreams:

            if dream["id"] == dream_id:
                return dream

        raise KeyError(dream_id)