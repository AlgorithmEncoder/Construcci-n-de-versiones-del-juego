"""
Activity logger.

Stores persistent global activity generated throughout the game.

The logger keeps activity entries in memory during execution and only
writes them to disk when save() is explicitly called.
"""

from __future__ import annotations

import json
import os

from datetime import datetime
from pathlib import Path

from constants import GLOBAL_DIR

# ============================================================

# Paths

# ============================================================

ACTIVITY_FILE = GLOBAL_DIR / "activity.json"

class Logger:
    
    """
    Activity logger.

    Stores persistent global activity generated throughout the game.

    The logger keeps activity entries in memory during execution and only
    writes them to disk when save() is explicitly called.
    """

    def __init__(self):

        self._entries: list[dict] = []

    # ========================================================
    # Public API
    # ========================================================

    def load(self) -> list[dict]:
        """
        Load the activity log from disk.

        If the file does not exist or contains invalid/empty data,
        an empty log is created in memory.

        Returns
        -------
        list[dict]
            Current activity entries.
        """

        self._entries = []

        if not ACTIVITY_FILE.exists():

            return self._entries

        try:

            with ACTIVITY_FILE.open(
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

        except (
            OSError,
            json.JSONDecodeError
        ):

            return self._entries

        if not isinstance(data, list):

            return self._entries

        self._entries = [

            entry

            for entry in data

            if isinstance(entry, dict)

        ]

        return self._entries

    # --------------------------------------------------------

    def register(
        self,
        message: str,
        *,
        category: str = "general"
    ) -> dict:
        """
        Register an activity entry in memory.

        The entry is NOT written to disk until save() is called.

        Parameters
        ----------
        message : str
            Human-readable description of the activity.

        category : str, optional
            Activity category.

        Returns
        -------
        dict
            The newly created activity entry.
        """

        entry = {

            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),

            "category": category,

            "message": str(message),

        }

        self._entries.append(entry)

        return entry

    # --------------------------------------------------------

    def save(self) -> bool:
        """
        Save the current activity log to disk.

        The file is written through a temporary file first and then
        replaced atomically when possible.

        Returns
        -------
        bool
            True if saving succeeded, False otherwise.
        """

        try:

            GLOBAL_DIR.mkdir(
                parents=True,
                exist_ok=True
            )

            temporary_file = ACTIVITY_FILE.with_suffix(
                ".tmp"
            )

            with temporary_file.open(
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self._entries,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

                file.write("\n")

            os.replace(
                temporary_file,
                ACTIVITY_FILE
            )

            return True

        except OSError:

            return False

    # ========================================================
    # Properties
    # ========================================================

    @property
    def entries(self) -> list[dict]:
        """
        Return the current activity entries.

        The returned list is the logger's in-memory list.
        """

        return self._entries

    @property
    def count(self) -> int:
        """
        Return the number of registered activities.
        """

        return len(self._entries)

    # ========================================================
    # Utility
    # ========================================================

    def clear(self):
        """
        Clear the activity currently held in memory.

        This does NOT modify the file on disk until save() is called.
        """

        self._entries.clear()

